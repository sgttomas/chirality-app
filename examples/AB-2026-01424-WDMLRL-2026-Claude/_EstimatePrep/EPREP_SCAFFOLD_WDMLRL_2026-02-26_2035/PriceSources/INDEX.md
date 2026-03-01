# PriceSources — INDEX (Snapshot)

## Header

- Execution root: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- Snapshot: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035`
- BOE scaffold: `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/Scaffold/BOE_Scaffold.md`
- Currency: `CAD`
- Base year: `2026`
- Region: `Central Alberta (Ferintosh / Camrose County)`
- Prepared: `2026-02-26T20:47:24-07:00`
- Status: `DRAFT (parametric baseline)`

## Data Quality Statement

This snapshot is a parametric baseline intended to bootstrap estimation. Replace LOW-confidence items with quotes as soon as feasible.

| Confidence | Meaning | Accuracy |
|---|---|---|
| HIGH | Confirmed parameter or fixed allowance | Exact |
| MEDIUM | Parametric rate or typical effort estimate | +/-20-30% |
| LOW | Allowance or rough parametric | +/-30-50% |

## File Inventory

| File | Rows | Primary consumer / used-by |
|---|---:|---|
| `Assumed_Project_Parameters.csv` | 18 | ESTIMATING + BOE |
| `Building_Envelope_Rates.csv` | 6 | ESTIMATING |
| `Construction_Labour_Rates.csv` | 10 | ESTIMATING |
| `Earthwork_Civil_Rates.csv` | 4 | ESTIMATING |
| `Electrical_System_Rates.csv` | 11 | ESTIMATING |
| `Equipment_Pricing.csv` | 4 | ESTIMATING |
| `Fees_Permits_Insurance.csv` | 12 | ESTIMATING |
| `Geotechnical_Investigation_Rates.csv` | 15 | ESTIMATING |
| `Interior_Architectural_Rates.csv` | 5 | ESTIMATING |
| `Level_of_Effort.csv` | 582 | ESTIMATING (effort-based costing) |
| `Mechanical_System_Rates.csv` | 8 | ESTIMATING |
| `Optional_Items_Pricing.csv` | 2 | ESTIMATING |
| `Parametric_Building_Rates.csv` | 2 | ESTIMATING |
| `Paving_Surfacing_Rates.csv` | 4 | ESTIMATING |
| `Professional_Design_Fees.csv` | 5 | ESTIMATING (fee-based method; optional) |
| `Professional_Staff_Rates.csv` | 25 | ESTIMATING |
| `Structural_Concrete_Rates.csv` | 8 | ESTIMATING |
| `Underground_Utility_Rates.csv` | 5 | ESTIMATING |
| `CBS_Taxonomy.csv` | 29 | ESTIMATING (CBS code assignment) |
| `CBS_Taxonomy.md` | -- | ESTIMATING (CBS usage instructions) |

## PS-ID → File Mapping

| PS-ID | File | Notes |
|---|---|---|
| `PS-STAFF` | `Professional_Staff_Rates.csv` | Staff hourly rates (roles) |
| `PS-LOE` | `Level_of_Effort.csv` | Deliverable × role hours matrix |
| `PS-PARAMS` | `Assumed_Project_Parameters.csv` | Project parameters and assumptions |
| `PS-LAB` | `Construction_Labour_Rates.csv` | Trade labour rates with burden |
| `PS-SC` | `Structural_Concrete_Rates.csv` | Concrete/rebar/formwork allowances |
| `PS-BE` | `Building_Envelope_Rates.csv` | Envelope + doors allowances |
| `PS-MS` | `Mechanical_System_Rates.csv` | Mechanical/HVAC allowances |
| `PS-ES` | `Electrical_System_Rates.csv` | Electrical/low-voltage allowances |
| `PS-EC` | `Earthwork_Civil_Rates.csv` | Earthworks allowances |
| `PS-PS` | `Paving_Surfacing_Rates.csv` | Surfacing allowances |
| `PS-UU` | `Underground_Utility_Rates.csv` | Underground utilities allowances |
| `PS-FP` | `Fees_Permits_Insurance.csv` | Bonding/insurance/permits allowances |
| `PS-GI` | `Geotechnical_Investigation_Rates.csv` | Geotechnical investigation rates |
| `PS-IA` | `Interior_Architectural_Rates.csv` | Interior build-out allowances |
| `PS-EQ` | `Equipment_Pricing.csv` | Major equipment allowances |
| `PS-OPT` | `Optional_Items_Pricing.csv` | Optional/contingency allowances |
| `PS-DF` | `Professional_Design_Fees.csv` | Design fee % (optional method) |
| `PS-PB` | `Parametric_Building_Rates.csv` | Parametric building cross-check rates |
| `PS-CBS` | `CBS_Taxonomy.csv` | Canonical CBS taxonomy (29 L2 categories) |

## ESTIMATING Run Configuration

### Deliverable-to-Package mapping

| Package | Deliverables |
|---|---|
| PKG-001 Architectural Design | DEL-001-01, DEL-001-02, DEL-001-03, DEL-001-04, DEL-001-05, DEL-001-06, DEL-001-07, DEL-001-08, DEL-001-09, DEL-001-10, DEL-001-11 |
| PKG-002 Structural Design | DEL-002-01, DEL-002-02, DEL-002-03, DEL-002-04, DEL-002-05, DEL-002-06, DEL-002-07, DEL-002-08, DEL-002-09, DEL-002-10, DEL-002-11, DEL-002-12 |
| PKG-003 Mechanical Design | DEL-003-01, DEL-003-02, DEL-003-03, DEL-003-04, DEL-003-05, DEL-003-06, DEL-003-07 |
| PKG-004 Electrical Design | DEL-004-01, DEL-004-02, DEL-004-03, DEL-004-04, DEL-004-05, DEL-004-06, DEL-004-07, DEL-004-08, DEL-004-09 |
| PKG-005 Civil Design | DEL-005-01, DEL-005-02, DEL-005-03, DEL-005-04, DEL-005-05, DEL-005-06, DEL-005-07 |
| PKG-006 Plumbing Design | DEL-006-01, DEL-006-02, DEL-006-03, DEL-006-04, DEL-006-05, DEL-006-06, DEL-006-07, DEL-006-08 |
| PKG-007 Landscape Architectural Design | DEL-007-01, DEL-007-02, DEL-007-03, DEL-007-04 |
| PKG-008 Geotechnical Investigation & Surveying | DEL-008-01, DEL-008-02, DEL-008-03, DEL-008-04 |
| PKG-009 Permitting & Regulatory Compliance | DEL-009-01, DEL-009-02, DEL-009-03, DEL-009-04 |
| PKG-010 Foundation Construction | DEL-010-01 |
| PKG-011 Building Structure & Envelope | DEL-011-01, DEL-011-02, DEL-011-03, DEL-011-04, DEL-011-05, DEL-011-06, DEL-011-07 |
| PKG-012 Interior Construction & Fit-Out | DEL-012-01, DEL-012-02, DEL-012-03 |
| PKG-013 Mechanical & HVAC Installation | DEL-013-01, DEL-013-02, DEL-013-03, DEL-013-04, DEL-013-05, DEL-013-06 |
| PKG-014 (Plumbing & Water Systems Installation) | DEL-014-01, DEL-014-02, DEL-014-03, DEL-014-04, DEL-014-05, DEL-014-06 |
| PKG-015 (Electrical & Low-Voltage Installation) | DEL-015-01, DEL-015-02, DEL-015-03, DEL-015-04, DEL-015-05 |
| PKG-016 (Crane & Lifting Equipment) | DEL-016-01 |
| PKG-017 (Existing Building Renovation - Old North Shop) | DEL-017-01, DEL-017-02, DEL-017-03, DEL-017-04 |
| PKG-018 (Sitework & Civil Construction) | DEL-018-01, DEL-018-02, DEL-018-03, DEL-018-04, DEL-018-05, DEL-018-06 |
| PKG-019 — Construction Management & OH&S | DEL-019-01, DEL-019-02, DEL-019-03, DEL-019-04 |
| PKG-020 — Commissioning & Closeout | DEL-020-01, DEL-020-02, DEL-020-03 |
| PKG-021 — Bonding, Insurance & Warranty | DEL-021-01, DEL-021-02, DEL-021-03, DEL-021-04, DEL-021-05 |

### Per-package PRICE_SOURCES mapping

| Package | PRICE_SOURCES (snapshot-relative paths) |
|---|---|
| PKG-001 Architectural Design | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Parametric_Building_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Fees_Permits_Insurance.csv` |
| PKG-002 Structural Design | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` |
| PKG-003 Mechanical Design | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` |
| PKG-004 Electrical Design | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` |
| PKG-005 Civil Design | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` |
| PKG-006 Plumbing Design | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` |
| PKG-007 Landscape Architectural Design | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` |
| PKG-008 Geotechnical Investigation & Surveying | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Geotechnical_Investigation_Rates.csv` |
| PKG-009 Permitting & Regulatory Compliance | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` |
| PKG-010 Foundation Construction | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Structural_Concrete_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Earthwork_Civil_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv` |
| PKG-011 Building Structure & Envelope | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Structural_Concrete_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Building_Envelope_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Equipment_Pricing.csv` |
| PKG-012 Interior Construction & Fit-Out | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Interior_Architectural_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv` |
| PKG-013 Mechanical & HVAC Installation | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Mechanical_System_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Equipment_Pricing.csv` |
| PKG-014 (Plumbing & Water Systems Installation) | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Underground_Utility_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Equipment_Pricing.csv` |
| PKG-015 (Electrical & Low-Voltage Installation) | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Electrical_System_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Underground_Utility_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv` |
| PKG-016 (Crane & Lifting Equipment) | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Equipment_Pricing.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv` |
| PKG-017 (Existing Building Renovation - Old North Shop) | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Interior_Architectural_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Mechanical_System_Rates.csv` |
| PKG-018 (Sitework & Civil Construction) | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Earthwork_Civil_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Paving_Surfacing_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Underground_Utility_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv` |
| PKG-019 — Construction Management & OH&S | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Fees_Permits_Insurance.csv` |
| PKG-020 — Commissioning & Closeout | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Optional_Items_Pricing.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Fees_Permits_Insurance.csv` |
| PKG-021 — Bonding, Insurance & Warranty | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`<br>`_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Fees_Permits_Insurance.csv` |

### ESTIMATING usage guidance

- Use `RecommendedRate` / `RecommendedPrice` / `RecommendedPercent` as point estimates.
- Flag `Confidence=LOW` items for early quote replacement.
- Record `Basis` and `Confidence` in estimate detail/provenance outputs.
- **CBS codes**: assign every line item a CBS value from `CBS_Taxonomy.csv` (PS-CBS). Use the `CBS_L2` value exactly as listed. See `CBS_Taxonomy.md` for full instructions and decision rules.

## Open Issues (estimation-impacting)

| IssueID | Description | Impact | Status |
|---|---|---|---|
| OI-001 | Foundation pricing is variable post-geotech | High | OPEN |
| OI-002 | Addition area/dimensions not extracted from drawing text layer | Medium | OPEN |
| OI-003 | Permit fee payment responsibility (Owner vs Proponent) requires confirmation | Medium | OPEN |

## Gaps / Quote Targets

| GapID | Item | Suggested workaround |
|---|---|---|
| GAP-001 | Overhead cranes (supply/install) | Carry allowance (EQ-01) and seek vendor quotes |
| GAP-002 | Make-up air unit sizing and cost | Carry allowance (MS-02) and obtain mechanical vendor budget quote |
| GAP-003 | Utility/service upgrade for 3-phase power | Carry allowance (ES-03) and confirm with utility/engineer |
