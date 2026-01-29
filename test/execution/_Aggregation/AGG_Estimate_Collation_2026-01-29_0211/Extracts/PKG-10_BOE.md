# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG10_DRAFT_2026-01-28_2401 |
| Estimate Label | PKG10_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-10 Railcar Unloading System (5 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-10:

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

### Scope Elements (from Decomposition PKG-10)

- **Unloading arms:** 32 articulating bottom-loading arms with swivel joints for railcar-to-header connection
- **Quick-connects:** 32 dry-break couplers for railcar bottom outlet connection
- **Gravity flow header:** Single collection header with 32 branch connections from unloading stations to storage
- **Spill containment pans:** 32 under-track containment pans with drainage and collection
- **Collection system:** Sumps, drains, sump pumps (8 units) for spill recovery
- **Atmospheric venting:** 32 vent connections and routing from railcars with flame arrestors
- **Flow indicators:** 32 local flow indication devices at each station

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Rail track construction (PKG-07) | Separate package; track alignment provided by PKG-07 |
| Process piping downstream of header (PKG-14) | Separate package; header discharge interface coordinated with PKG-14 |
| Storage tanks (PKG-13) | Separate package; header delivers to tank farm |
| Custody transfer metering (PKG-12) | Separate package; metering at rail unload and marine load |
| Control system integration (PKG-19) | Separate package; control interfaces coordinated |
| Field instrumentation beyond flow indicators (PKG-20) | Separate package; instrumentation interfaces coordinated |
| Electrical distribution to pumps (PKG-17) | Separate package; electrical interfaces coordinated |
| Nitrogen supply skid | Employer-supplied per decomposition Section 1.2 |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design, procurement, installation | decomposition Section 1.2 |
| Rail track interface | Track alignment and railcar positioning provided by PKG-07 | D-002 |
| Header discharge interface | Downstream piping connection coordinated with PKG-14 | D-003 |
| Unloading arm type | Bottom-loading articulating arms (assumption based on gravity flow) | A-001 |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-004 |
| Site access | Adjacent to rail tracks; standard construction access | D-005 |
| Working hours | Standard 8-10 hour shifts; minimal constraints | D-006 |
| Seasonal constraints | Year-round construction feasible; winterization may affect operations | A-028 |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-007 — All pricing uses allowances due to absence of vendor quotes or rate tables.

## Quantity Basis

Quantities are parametric estimates based on:
- Decomposition scope statement: 32 railcar unloading stations (Section 1 Key Parameters)
- Deliverable document scope descriptions (DEL-10.01, DEL-10.02, DEL-10.04 Datasheets)
- Industry-standard railcar unloading system configurations
- Typical gravity flow header arrangement for multi-station systems

| Item | Estimated Quantity | Basis | Decision Ref |
|------|-------------------|-------|--------------|
| Unloading arms | 32 units | Per decomposition: 32 railcar unloading stations | decomposition Section 1 |
| Quick-connect couplers | 32 units | One per unloading arm | decomposition Section 5 PKG-10 |
| Gravity flow header piping | 400 lm | Estimated header length for 32-station layout (~12m spacing avg + routing) | A-003 |
| Spill containment pans | 32 units | Individual pans per station (one per arm) | A-004 |
| Sump pumps | 8 units | Grouped containment zones (4 pumps per zone × 2 zones) | A-005 |
| Flow indicators | 32 units | One per unloading station | DEL-10.04 Datasheet |
| Atmospheric vent connections | 32 units | One per railcar unloading station | DEL-10.01 Datasheet |

## Indirects Model

**Method:** Factor-based (fallback typical model)

| Factor | Rate | Base | Decision Ref |
|--------|------|------|--------------|
| Construction Indirects (CI) | 0.18 | CD | D-008 |
| Procurement Services (P) | 0.02 | MAT | D-008 |
| EPCM/PM | 0.06 | CD + CI + MAT | D-008 |
| Commissioning (COM) | N/A | Line item allowances | D-008 |

**Note:** Commissioning costs estimated via line item allowances for FAT, system integration testing, performance verification per deliverable requirements rather than factor-based method.

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket)

| CBS | Base % | Allowance Adjustment | Final % | Rationale |
|-----|--------|---------------------|---------|-----------|
| E | 10% | +10% (100% allowance) | 20% | All engineering allowances |
| MAT | 15% | +10% (100% allowance) | 25% | All material allowances; specialized unloading equipment |
| CD | 20% | +10% (100% allowance) | 30% | All CD allowances; specialized installation |
| CI | 20% | +10% (factor-derived) | 30% | Derived from CD |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (allowance-based) | 30% | Allowance-based; system integration testing risk |

**Decision:** D-009 — Contingency rates elevated due to 100% allowance-based estimate and specialized railcar unloading equipment.

## Escalation Method

- **Mode:** NONE
- **Rationale:** Pricing date is current (January 2026); no escalation applied per config
- **Decision:** D-010

## Rounding Policy

- **Rounding:** Nearest $1,000 CAD
- **Decision:** Per _CONFIG.md

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Lines priced by QUOTE | 0% |
| Lines priced by RATE_TABLE | 0% |
| Lines priced by ALLOWANCE/PARAMETRIC | 100% |
| Deliverables with explicit quantities | 20% (1 of 5) |
| Overall confidence | LOW |

## Known Gaps

| Gap | Impact | Resolution Path |
|-----|--------|-----------------|
| No railcar unloading arm vendor quotes | Arm pricing based on industry typical ranges | Obtain budgetary quotes from specialized suppliers (TechnipFMC, OPW, etc.) |
| No PKG-07 track layout details (DEL-07.01) | Station spacing and positioning assumed | Provide PKG-07 rail track alignment drawings |
| No product data sheets for canola oil | Viscosity/temperature assumptions affect header sizing | Obtain canola oil product specifications from Employer |
| No DEL-10.03 calculations completed | Header sizing and simultaneous operations not verified | Progress DEL-10.03 to verify throughput capacity |
| No regulatory containment requirements | Containment volume based on typical requirements | Obtain applicable environmental regulations |
| No rate tables | Labor rates assumed | Provide project rate library |
| No PKG-14 interface details | Header discharge connection assumed | Coordinate header-to-storage piping interface with PKG-14 |
| No hazardous area classification | Equipment area rating assumptions | Provide HAC study results |

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-010 |
| Assumptions_Log.md | All assumptions A-001 through A-030+ |
| Detail.csv | Line item detail with traceability |
| Summary.md | Cost summaries and confidence metrics |
