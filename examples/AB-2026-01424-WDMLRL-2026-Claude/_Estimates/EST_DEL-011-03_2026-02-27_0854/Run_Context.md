# Run Context — EST_DEL-011-03_2026-02-27_0854

| Field | Value |
|---|---|
| **RunID** | EST_DEL-011-03_2026-02-27_0854 |
| **AsOf** | 2026-02-27T08:54:00Z |
| **Scope** | DEL-011-03 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-011-03 Drive-Through Repair Bays) in PKG-011 Building Structure & Envelope |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Structural_Concrete_Rates.csv, Building_Envelope_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **OUTPUT_LABEL** | DEL-011-03 |
| **Rounding** | NONE (default) |

## Resolved Defaults

- `RUN_TIMESTAMP`: 2026-02-27T08:54:00Z (generated at runtime)
- `ROUNDING`: NONE (default)
- `FALLBACK_POLICY`: ALLOW_PARAMETRIC -- permits parametric pricing where basis evidence exists in pricing source tables
- `ALLOW_MIXED_METHODS`: TRUE -- allows PARAMETRIC and ALLOWANCE methods to coexist in Detail.csv

## Warnings

- W-01: Overhead door finished dimensions (width and height) are TBD per IFC drawings. Pricing uses BE-03 24' class overhead door rate ($19,000 each) as parametric benchmark.
- W-02: Door height (estimated 14-16 ft for motor scraper class equipment) is TBD pending IFC drawings and County fleet data. Door pricing may change based on actual height specification.
- W-03: Door type (sectional vs. rolling steel) is TBD in IFC drawings. Parametric rate assumes industrial sectional overhead doors.
- W-04: Bay width dimension (nominal 24') is not yet confirmed as clear opening width vs. structural bay width. See Datasheet Normalization Note.
- W-05: Door operator specifications (motor type, voltage, amperage) are TBD per IFC door schedule. Operator cost included in overhead door allowance.
- W-06: Oil/water separator requirement for repair bay floor drainage is TBD per Alberta environmental regulations (Guidance CT-002). If required, additional structural slab provisions may be needed.
- W-07: Fire separation requirements between repair bays and adjacent spaces TBD per design team assessment (Guidance CT-003/Lensing F-002).
