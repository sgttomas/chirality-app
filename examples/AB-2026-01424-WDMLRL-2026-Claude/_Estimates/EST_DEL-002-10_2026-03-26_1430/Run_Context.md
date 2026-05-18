# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-002-10_2026-03-26_1430 |
| **AsOf** | 2026-03-26T14:30:00Z |
| **Scope** | DEL-002-10 (Structural Calculation Package) |
| **ScopeResolvedSummary** | 1 deliverable, 1 package (PKG-002 Structural Design) |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, CBS_Taxonomy.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md (R2 -- 2026-03-26, SCA-001) |
| **DEPENDENCY_SOURCES** | AUTO (DEL-002-10/Dependencies.csv) |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE |
| **OUTPUT_LABEL** | DEL-002-10 |

## Prior Estimate Reference

| Field | Value |
|---|---|
| **Prior RunID** | EST_DEL-002-10_2026-02-26_2239 |
| **Prior Total** | $13,330 CAD |
| **Prior Basis** | PARAMETRIC |
| **Staleness Reason** | Post-SCA-001 refresh required |

## Staleness Triggers (SCA-001)

1. **Structural system changed** from monolithic concrete to precast concrete walls + steel roof (Add. 2, Add. 4). This creates a hybrid structural system requiring calculation work across two material standards (CSA A23.3 for precast concrete, CSA S16 for steel roof framing). Additional calculation sections are needed for precast panel connection design, steel roof member design, and hybrid lateral system analysis.
2. **Crane corbel loads now defined** (Add. 4, Q3). Crane support is corbel-mounted on precast wall panels. This requires explicit corbel design calculations (previously implicit in a monolithic concrete wall system) and verification of precast panel adequacy under concentrated crane loads.
3. **Interior walls specified as precast concrete** (Add. 4, Q5). Interior precast walls require structural calculation for self-weight, connection to primary structure, and seismic anchorage -- scope not present in the original monolithic concrete assumption.

## Resolved Price Source Paths

| Source | Absolute Path | Type |
|---|---|---|
| Professional_Staff_Rates.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | Rate Table (hourly rates by role) |
| Level_of_Effort.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | Parametric (hours by deliverable and role -- baseline, pre-SCA-001) |
| CBS_Taxonomy.csv | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/CBS_Taxonomy.csv` | CBS code assignment reference |

## CBS Mapping Rule

CBS codes assigned per CBS_Taxonomy.csv:
- CBS-01 (Professional Services > Design & Engineering) for all design/engineering labour
- CBS-02 (Professional Services > Project Management) for PM and cost estimator labour

## Scope Notes

- DEL-002-10 is the Structural Calculation Package under PKG-002 Structural Design.
- SOW coverage: SOW-0012 (structural design -- precast concrete walls + steel roof per Add. 2/4), SOW-0019 (foundation variable-price scope).
- Deliverable type: Calculation Package (professional engineering labor only).
- Structural subsystems: 8 primary (Concrete Superstructure, Foundation, Mezzanine, Crane Support, Steel Plate Embedments, Service Pit, Wash Bay, Stairs) plus new sub-items for precast connections, steel roof framing, corbel design, and interior precast wall analysis.

## Hour Adjustment Rationale (RATE_TABLE baseline + ALLOWANCE supplements)

The LOE.csv baseline hours (90 total) were prepared before SCA-001 and reflect a monolithic concrete structural system. The hybrid precast concrete walls + steel roof system (Add. 2/4) materially increases calculation complexity:

1. **Steel roof framing calculations** -- new scope not in original LOE (steel member selection, connection design per CSA S16, roof diaphragm analysis). Estimated +16 hrs Structural Engineer, +8 hrs BIM Technician.
2. **Precast wall panel connection design** -- panel-to-panel, panel-to-foundation, panel-to-steel-roof connections require explicit calculation (not needed for monolithic concrete). Estimated +12 hrs Structural Engineer, +4 hrs BIM Technician.
3. **Crane corbel design** -- dedicated calculation section for corbel bracket design cast into precast panels, including local panel stress checks. Estimated +8 hrs Structural Engineer.
4. **Interior precast wall analysis** -- self-weight, seismic anchorage, and connection to primary structure. Estimated +6 hrs Structural Engineer, +2 hrs BIM Technician.
5. **Additional PM coordination** -- hybrid system requires coordination with precast supplier and steel fabricator. Estimated +4 hrs PM.

Total adjustment: +42 hrs Structural Engineer, +14 hrs BIM Technician, +4 hrs PM.

## Warnings

- LOE.csv hours are pre-SCA-001 and do not reflect the hybrid structural system. Adjustments applied as ALLOWANCE line items.
- All rates remain MEDIUM confidence parametric estimates from Professional_Staff_Rates.csv.
- Hour adjustments for scope changes are ALLOWANCE-method estimates with LOW confidence pending actual design effort tracking.
