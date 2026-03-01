# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-011-05_2026-02-27_0848 |
| **AsOf** | 2026-02-27T08:48Z |
| **Scope** | DEL-011-05 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-011-05 Wash Bay Enclosure) in PKG-011 Building Structure & Envelope |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Structural_Concrete_Rates.csv, Building_Envelope_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-011-05 |

## Warnings

- Multiple TBD attributes in Datasheet (steel plate dimensions, wall material, overhead door height, clear ceiling height, floor drainage slope) reduce pricing confidence.
- Steel plate scope ownership conflict (C-01 in Guidance Conflict Table) may result in double-counting or omission across DEL-011-05 and DEL-011-02; this estimate includes wash bay steel plate as part of DEL-011-05 scope per SOW-0027a.
- Gantry provisions are conditional (ASSUMPTION, not confirmed); included as a conditional allowance.
- Equipment_Pricing items EQ-02 (pressure washer) and EQ-03 (air compressor) are excluded from this deliverable scope (they are building-wide equipment, not specific to the wash bay enclosure structure).
