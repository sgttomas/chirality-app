# PRICE_SOURCES Index — Execution 6b
## Proposal Production Cost Estimating (Discipline-Split)

**Execution Root:** `test/execution-6b/`
**BOE:** `test/execution-6b/_Estimates/BASIS_OF_ESTIMATE.md`
**Currency:** CAD | **Base Year:** 2024 | **Region:** Alberta (Penhold/Red Deer)
**Prepared:** 2026-02-18
**Status:** DRAFT — Parametric and market-based estimates; no vendor quotes

---

## Data Quality Statement

All rates are **parametric estimates based on Alberta 2024 market data**. Professional hourly rates reflect typical Design-Build firm internal rates. Level-of-effort hours are planning estimates based on comparable proposal efforts for $15-20M municipal DB projects.

| Confidence | Meaning | Accuracy |
|-----------|---------|----------|
| HIGH | Confirmed parameter or fixed allowance | Exact |
| MEDIUM | Parametric rate or typical effort estimate | +/-20-30% |
| LOW | Allowance or rough parametric | +/-30-50% |

---

## File Inventory

### Primary files (proposal production costing)

| File | Items | Used By |
|------|-------|---------|
| `Professional_Staff_Rates.csv` | 30 roles | All 38 deliverables — hourly rates for proposal production roles |
| `Level_of_Effort.csv` | 72 rows | All 38 deliverables — hours per role per deliverable |
| `Assumed_Project_Parameters.csv` | 29 params | PP-04 (proposal timeline), PP-05-08 (areas for scope calibration) |
| `Fees_Permits_Insurance.csv` | 19 items | DEL-01-03 (bond/insurance premiums) |

### Construction pricing files (for Schedule A/B content in DEL-01-04, DEL-01-05)

These files provide the construction pricing that gets embedded IN the Schedule A and Schedule B forms. This is the proposal PRICE, not the proposal PRODUCTION cost.

| File | Items | Used By |
|------|-------|---------|
| `Structural_Concrete_Rates.csv` | 15 items | Schedule A/B structural scope |
| `Building_Envelope_Rates.csv` | 15 items | Schedule A/B envelope scope |
| `Mechanical_System_Rates.csv` | 14 items | Schedule A/B mechanical scope |
| `Electrical_System_Rates.csv` | 14 items | Schedule A/B electrical scope |
| `Earthwork_Civil_Rates.csv` | 11 items | Schedule A/B site/civil scope |
| `Paving_Surfacing_Rates.csv` | 9 items | Schedule A/B paving scope |
| `Underground_Utility_Rates.csv` | 12 items | Schedule A/B utility scope |
| `Equipment_Pricing.csv` | 15 items | Schedule A/B equipment line items |
| `Optional_Items_Pricing.csv` | 18 items | Schedule A/B optional items (Options 1-6) |
| `Interior_Architectural_Rates.csv` | 25 items | Schedule A/B interior scope (partitions, ceilings, flooring, paint, accessibility, signage, millwork, specialties) |
| `Parametric_Building_Rates.csv` | 9 items | Parametric cross-check of Schedule A totals |
| `Construction_Labour_Rates.csv` | 15 trades | Schedule A/B labour rates |
| `Professional_Design_Fees.csv` | 8 items | Schedule A/B design fee line items |

---

## BOE PS-ID → File Mapping

| PS-ID | Source | File | Key Items |
|-------|--------|------|-----------|
| PS-01 | Proposal staff rate table | `Professional_Staff_Rates.csv` | All R-xx roles applicable to proposal production |
| PS-02 | Production hours per deliverable | `Level_of_Effort.csv` | 72 rows: 38 deliverables x applicable roles |
| PS-03 | Proposal preparation timeline | `Assumed_Project_Parameters.csv` | PP-04 (6 weeks) |
| PS-04 | Construction pricing for Schedule A/B | All construction rate files listed above | Full construction pricing library for DEL-01-04/05 content |
| PS-13 | Interior architectural | `Interior_Architectural_Rates.csv` | IA-01 through IA-25 (partitions, ceilings, flooring, paint, accessibility, signage, millwork, specialties) |
| PS-05 | CCIP insurance premium | `Fees_Permits_Insurance.csv` | FP-03 (1.5-2.5%) |
| PS-06 | Bond premium rate | `Fees_Permits_Insurance.csv` | FP-01 (performance 1.5%) + FP-02 (L&M 1.0%) |
| PS-07 | Surety broker fee | `Fees_Permits_Insurance.csv` | FP-19 ($2000-5000) |
| PS-08 | Legal review hourly rate | `Professional_Staff_Rates.csv` | R-25 ($300/hr) |
| PS-09 | CAD/BIM software costs | N/A | Embedded in R-06 hourly rate |
| PS-10 | Scheduling software costs | N/A | Embedded in R-17 hourly rate |
| PS-11 | 3D rendering costs | N/A | Optional: 16-24 hours of R-06 time |
| PS-12 | Printing/reproduction | N/A | Digital submission; negligible |

---

## ESTIMATING Run Configuration

### For proposal production deliverables (33 of 38)

Most deliverables are pure proposal production cost. For these, ESTIMATING computes:
`Cost = Σ (Hours_per_role × Hourly_rate_per_role)`

```
PRICE_SOURCES:
  - "{EXECUTION_ROOT}/_PriceSources/Professional_Staff_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Level_of_Effort.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Assumed_Project_Parameters.csv"
```

### For DEL-01-04 (Schedule A) and DEL-01-05 (Schedule B)

These have DUAL cost nature — production hours PLUS embedded construction pricing:

```
PRICE_SOURCES:
  - "{EXECUTION_ROOT}/_PriceSources/Professional_Staff_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Level_of_Effort.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Structural_Concrete_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Building_Envelope_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Interior_Architectural_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Mechanical_System_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Electrical_System_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Earthwork_Civil_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Paving_Surfacing_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Underground_Utility_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Equipment_Pricing.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Optional_Items_Pricing.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Parametric_Building_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Construction_Labour_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Professional_Design_Fees.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Fees_Permits_Insurance.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Assumed_Project_Parameters.csv"
```

ESTIMATING must produce two line groups in Detail.csv:
1. **Production cost lines** (Method=RATE_TABLE): estimator/PM hours × rates
2. **Construction pricing content lines** (Method=PARAMETRIC/RATE_TABLE/QUOTE/ALLOWANCE): the actual proposal prices

### For DEL-01-03 (Bonding & Insurance)

```
PRICE_SOURCES:
  - "{EXECUTION_ROOT}/_PriceSources/Professional_Staff_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Level_of_Effort.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Fees_Permits_Insurance.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Assumed_Project_Parameters.csv"
```

### Per-package source mapping (proposal production)

| Package | Primary PRICE_SOURCES |
|---------|----------------------|
| PKG-001 | Staff_Rates, LOE, Parameters, Fees (for DEL-01-03/04/05) |
| PKG-002 | Staff_Rates, LOE, Parameters |
| PKG-003 | Staff_Rates, LOE, Parameters |
| PKG-004 | Staff_Rates, LOE, Parameters |
| PKG-005 | Staff_Rates, LOE, Parameters |
| PKG-006 | Staff_Rates, LOE, Parameters |
| PKG-007 | Staff_Rates, LOE, Parameters |
| PKG-008 | Staff_Rates, LOE, Parameters |
| PKG-009 | Staff_Rates, LOE, Parameters |
| PKG-010 | Staff_Rates, LOE, Parameters |

---

## Gaps Requiring Parametric Estimation

| Gap | ESTIMATING Workaround |
|-----|----------------------|
| Actual DB firm hourly rates | Use parametric Alberta market rates from Professional_Staff_Rates.csv |
| Actual effort per deliverable | Use LOE estimates; flag as PARAMETRIC in Detail.csv |
| CCIP insurance actual premium | Use FP-03 (2.0%) until actual quote |
| Bond premium actual rate | Use FP-01 + FP-02 (2.5% combined) until actual quote |
| Construction pricing for Schedule A/B | Use construction rate files; flag all as PARAMETRIC |
| Proposal timeline (may compress/extend) | Use PP-04 (6 weeks); adjust coordination overhead if timeline changes |

---

**END OF DOCUMENT**
