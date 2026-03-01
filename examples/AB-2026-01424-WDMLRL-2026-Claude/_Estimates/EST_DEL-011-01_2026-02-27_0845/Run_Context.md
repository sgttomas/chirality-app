# Run Context — EST_DEL-011-01_2026-02-27_0845

| Field | Value |
|---|---|
| **RunID** | EST_DEL-011-01_2026-02-27_0845 |
| **AsOf** | 2026-02-27T08:45:00Z |
| **Scope** | DEL-011-01 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-011-01 Concrete Superstructure) in PKG-011 Building Structure & Envelope |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Structural_Concrete_Rates.csv, Building_Envelope_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **OUTPUT_LABEL** | DEL-011-01 |
| **Rounding** | NONE (default) |

## Resolved Defaults

- `RUN_TIMESTAMP`: 2026-02-27T08:45:00Z (generated at runtime)
- `ROUNDING`: NONE (default)
- `FALLBACK_POLICY`: ALLOW_PARAMETRIC -- permits parametric pricing where basis evidence exists in pricing source tables
- `ALLOW_MIXED_METHODS`: TRUE -- allows PARAMETRIC and ALLOWANCE methods to coexist in Detail.csv

## Warnings

- W-01: Concrete compressive strength (f'c) is TBD per Structural Engineer of Record; slab and structural element unit rates use parametric benchmarks assuming typical industrial f'c (25-35 MPa).
- W-02: Structural system type (cast-in-place vs. tilt-up vs. precast) is TBD; parametric rates assume cast-in-place as baseline.
- W-03: Roof structure system is TBD; parametric rates assume a steel deck/bar joist system on concrete structure.
- W-04: Mezzanine design load is TBD; mezzanine rates assume heavy industrial storage classification.
- W-05: Several overhead door sizes are TBD; using parametric rates from Building_Envelope_Rates.csv.
- W-06: Geotechnical conditions not yet confirmed; superstructure rates assume normal ground conditions.
- W-07: Building footprint area derived from conceptual drawing (130 ft x 100 ft = 12,077 m2 approx 1,208 m2). Confirmation with County pending.
