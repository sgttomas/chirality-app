# Run Context — EST_DEL-018-04_2026-02-27_0834

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-018-04_2026-02-27_0834 |
| **AsOf** | 2026-02-27T08:34:00Z |
| **Scope** | DEL-018-04 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-018-04 — Cement & Gravel Pads), 1 package (PKG-018 — Sitework & Civil Construction) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Earthwork_Civil_Rates.csv, Paving_Surfacing_Rates.csv, Underground_Utility_Rates.csv, Construction_Labour_Rates.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-018-04 |

## Resolved Defaults

- RUN_TIMESTAMP generated at runtime (2026-02-27T08:34:00Z).
- Rounding: NONE (no rounding directive provided; default applied).
- UPDATE_LATEST_POINTER: FALSE (pointer file not modified).
- FALLBACK_POLICY: ALLOW_PARAMETRIC — items without direct quote or rate table evidence may be priced using parametric models from the provided price sources.
- ALLOW_MIXED_METHODS: TRUE — Detail.csv may contain a mix of methods where supported.

## Warnings

- W-001: Cement pad area dimensions are partially TBD. South zone cement pad has one annotated dimension (18') from Appendix B; width is not stated. A parametric assumption of ~130' width (matching New North Shop width) is used. IFC civil drawings will govern.
- W-002: Small east-side cement pad near wash bay has no stated dimensions. A parametric allowance of ~14 m2 is assumed.
- W-003: Gravel pad fill depth/thickness is TBD pending IFC civil drawings and geotechnical report. A parametric depth of 300mm (0.30 m) is assumed for volume calculation.
- W-004: Concrete mix design, reinforcement, and specific pad thickness are TBD. Pricing uses Paving_Surfacing_Rates.csv PS-03 (concrete apron/approach slab, $190/m2) as a parametric proxy.
- W-005: County/Landfill supplies gravel for gravel pad (SOW-0203); material cost for gravel pad fill is excluded from this estimate. Contractor cost covers subgrade prep, placement, and compaction only.
- W-006: Crane pad structural requirements (thickened slab, reinforcement for 5-tonne crane loads) are TBD pending crane supplier data and P.Eng. design. A parametric uplift factor is applied.
