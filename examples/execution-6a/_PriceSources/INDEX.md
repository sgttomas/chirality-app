# PRICE_SOURCES Index — Execution 6a
## Physical-Scope Construction Estimating

**Execution Root:** `test/execution-6a/`
**BOE:** `test/execution-6a/_Estimates/BASIS_OF_ESTIMATE.md`
**Currency:** CAD | **Base Year:** 2024 | **Region:** Alberta (Penhold/Red Deer)
**Prepared:** 2026-02-18
**Status:** DRAFT — Parametric and market-based estimates; no vendor quotes

---

## Data Quality Statement

All rates are **parametric estimates based on Alberta 2024 construction market data**. No vendor-specific quotes. Suitable for Class 4-5 (conceptual/order-of-magnitude) estimating.

| Confidence | Meaning | Accuracy |
|-----------|---------|----------|
| HIGH | Confirmed parameter or fixed allowance | Exact |
| MEDIUM | Parametric rate from market data | +/-20-30% |
| LOW | Allowance or rough parametric | +/-30-50% |

Use `RecommendedRate` as the point estimate. Flag `Confidence=LOW` items in QA_Report for future vendor quote replacement.

---

## File Inventory

| File | Items | Used By |
|------|-------|---------|
| `Professional_Staff_Rates.csv` | 30 roles | PKG-001 management rates; design fee role rates |
| `Construction_Labour_Rates.csv` | 15 trades | All construction packages |
| `Structural_Concrete_Rates.csv` | 15 items | DEL-02-04, DEL-04-03 |
| `Building_Envelope_Rates.csv` | 15 items | DEL-02-04, DEL-04-01 |
| `Mechanical_System_Rates.csv` | 14 items | DEL-02-05, DEL-04-04 |
| `Electrical_System_Rates.csv` | 14 items | DEL-02-06, DEL-04-04 |
| `Earthwork_Civil_Rates.csv` | 11 items | DEL-03-02 |
| `Paving_Surfacing_Rates.csv` | 9 items | DEL-03-03 |
| `Underground_Utility_Rates.csv` | 12 items | DEL-03-04 |
| `Equipment_Pricing.csv` | 15 items | DEL-02-02, DEL-02-03, DEL-02-07 |
| `Optional_Items_Pricing.csv` | 18 items | PKG-005 (DEL-05-01 through DEL-05-07) |
| `Interior_Architectural_Rates.csv` | 25 items | DEL-02-01 (partitions, ceilings, flooring, paint, accessibility, signage, millwork, specialties) |
| `Parametric_Building_Rates.csv` | 9 items | DEL-04-01 (cold storage); parametric cross-check all |
| `Fees_Permits_Insurance.csv` | 19 items | DEL-01-04 (permits); DEL-03-05 (environmental) |
| `Professional_Design_Fees.csv` | 8 items | Design fee allocation in PKG-002/003/004 |
| `Assumed_Project_Parameters.csv` | 29 params | All deliverables — areas, quantities, durations |
| `Level_of_Effort.csv` | 17 rows | PKG-001 management hours (DEL-01-01 through DEL-01-07) |

---

## BOE PS-ID → File Mapping

| PS-ID | Source | File | Key Items |
|-------|--------|------|-----------|
| PS-01 | DB staff rate table | `Professional_Staff_Rates.csv` + `Level_of_Effort.csv` | R-01 through R-30; LOE for PKG-001 management hours |
| PS-02 | Project duration | `Assumed_Project_Parameters.csv` | PP-01 (18mo), PP-02 (4mo design), PP-03 (22mo total) |
| PS-03 | Structural steel/concrete | `Structural_Concrete_Rates.csv` | SC-01 through SC-15 |
| PS-04 | Pre-engineered metal building | `Parametric_Building_Rates.csv` | PB-01 ($28-35/sf shell), PB-02 ($42-55/sf turnkey) |
| PS-05 | Building envelope | `Building_Envelope_Rates.csv` | BE-01 through BE-15 |
| PS-27 | Interior architectural | `Interior_Architectural_Rates.csv` | IA-01 through IA-25 (partitions, ceilings, flooring, paint, accessibility, signage, millwork, specialties) |
| PS-06 | Mechanical systems | `Mechanical_System_Rates.csv` | MS-01 through MS-14 |
| PS-07 | Electrical systems | `Electrical_System_Rates.csv` | ES-01 through ES-14 |
| PS-08 | Earthwork | `Earthwork_Civil_Rates.csv` | EC-01 through EC-11 |
| PS-09 | Paving | `Paving_Surfacing_Rates.csv` | All items |
| PS-10 | Underground utilities | `Underground_Utility_Rates.csv` | UU-01 through UU-12; UU-12 = DEC-004 tie-in allowance |
| PS-11 | Overhead doors | `Equipment_Pricing.csv` | EQ-01 (car-wash, 8 units), EQ-02 (standard, 2 units) |
| PS-12 | Diesel generator | `Equipment_Pricing.csv` | EQ-04 ($120k-180k system) |
| PS-13 | Vehicle exhaust | `Mechanical_System_Rates.csv` | MS-06 ($22-28k/apparatus bay), MS-07 ($8-14k/shop bay) |
| PS-14 | Bunker gear lockers | `Equipment_Pricing.csv` | EQ-06 ($1800-2500 each, 40 units) |
| PS-15 | PW lockers | `Equipment_Pricing.csv` | EQ-07 ($800-1200 each, 40 units) |
| PS-16 | Breathing air compressor | `Equipment_Pricing.csv` | EQ-08 ($45k-65k system) |
| PS-17 | Bay sump assemblies | `Equipment_Pricing.csv` | EQ-10 ($3500-5500 each, 8 units) |
| PS-18 | Permit fees | `Fees_Permits_Insurance.csv` | FP-06 through FP-10 |
| PS-19 | Environmental consultant | `Fees_Permits_Insurance.csv` | FP-16, FP-17, FP-18 |
| PS-20 | Cold storage foundations | `Structural_Concrete_Rates.csv` | SC-12 (spread), SC-13 (strip), SC-14 (screw piles) |
| PS-21 | Wash bay | `Optional_Items_Pricing.csv` | OPT-01 through OPT-03 |
| PS-22 | Yard lighting | `Optional_Items_Pricing.csv` | OPT-04, OPT-05 |
| PS-23 | Access control | `Optional_Items_Pricing.csv` | OPT-06, OPT-07 |
| PS-24 | Security cameras | `Optional_Items_Pricing.csv` | OPT-08, OPT-09 |
| PS-25 | Signage | `Optional_Items_Pricing.csv` | OPT-10, OPT-11 — **BLOCKED: Town branding PENDING** |
| PS-26 | Appliances | `Optional_Items_Pricing.csv` | OPT-12 through OPT-17 |

---

## ESTIMATING Run Configuration

For each ESTIMATING INIT-TASK brief, set:

```
PRICE_SOURCES:
  - "{EXECUTION_ROOT}/_PriceSources/Professional_Staff_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Level_of_Effort.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Assumed_Project_Parameters.csv"
  - "{EXECUTION_ROOT}/_PriceSources/{applicable_rate_file}.csv"
```

### Per-package source mapping

| Package | PRICE_SOURCES files to load |
|---------|---------------------------|
| PKG-001 | Professional_Staff_Rates, Level_of_Effort, Assumed_Project_Parameters |
| PKG-002 | Structural_Concrete_Rates, Building_Envelope_Rates, Interior_Architectural_Rates, Mechanical_System_Rates, Electrical_System_Rates, Equipment_Pricing, Professional_Design_Fees, Assumed_Project_Parameters |
| PKG-003 | Earthwork_Civil_Rates, Paving_Surfacing_Rates, Underground_Utility_Rates, Fees_Permits_Insurance, Assumed_Project_Parameters |
| PKG-004 | Structural_Concrete_Rates, Building_Envelope_Rates, Mechanical_System_Rates, Electrical_System_Rates, Parametric_Building_Rates, Assumed_Project_Parameters |
| PKG-005 | Optional_Items_Pricing, Assumed_Project_Parameters |

---

## Gaps Requiring Parametric Estimation

| Gap | ESTIMATING Workaround |
|-----|----------------------|
| Town of Penhold fee schedules | Use Alberta municipal averages from Fees_Permits_Insurance.csv |
| Vendor quotes (generator, breathing air, doors) | Use parametric ranges; flag for future quote |
| Exact building dimensions | Use Assumed_Project_Parameters.csv PP-05 through PP-08 |
| Utility tie-in allowance (DEC-004) | Use UU-12 ($35,000 recommended); **Owner must confirm** |
| CCIP insurance premium | Use FP-03 (2.0%); actual quote needed |
| Generator 72-hour runtime | Assumed per PP-26; **Owner must confirm** |
| Town branding guidelines | Carry signage as allowance OPT-10/OPT-11 |
| Interior architectural rates (RESOLVED) | Added `Interior_Architectural_Rates.csv` (PS-27) with 25 items covering partitions, ceilings, flooring, paint, accessibility, signage, millwork, specialties |

---

**END OF DOCUMENT**
