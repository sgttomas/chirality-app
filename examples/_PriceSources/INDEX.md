# PRICE_SOURCES Index — Penhold PSB Project
## Shared Pricing Library for All Execution Versions

**Location:** `test/_PriceSources/`
**Currency:** CAD
**Base Year:** 2024
**Region:** Alberta, Canada (Central Alberta — Penhold/Red Deer area)
**Prepared:** 2026-02-18
**Status:** DRAFT — Parametric and market-based estimates; no vendor quotes

---

## Data Quality Statement

This pricing library uses **parametric estimates based on Alberta 2024 construction market data**. No vendor-specific quotes have been obtained. All rates should be treated as planning-grade estimates suitable for Class 4-5 (conceptual/order-of-magnitude) estimating.

| Confidence Level | Meaning | Typical Accuracy |
|-----------------|---------|-----------------|
| **HIGH** | Confirmed project parameter or fixed allowance | Exact |
| **MEDIUM** | Parametric rate from market data; reasonable for planning | +/-20-30% |
| **LOW** | Allowance or rough parametric; high variability expected | +/-30-50% |

**ESTIMATING agent instruction:** Where rates are given as min/max ranges, use the `RecommendedRate` column as the point estimate. Flag items with `Confidence=LOW` in the QA_Report for future vendor quote replacement. For items marked `Basis=ALLOWANCE`, explicitly note in Decision_Log.md that the value is a placeholder.

---

## File Inventory

| File | Contents | Primary Consumer |
|------|----------|-----------------|
| `Professional_Staff_Rates.csv` | 30 roles with hourly rates (A/E/PM/construction/admin/specialty) | All three executions |
| `Construction_Labour_Rates.csv` | 15 construction trades with fully-burdened rates | 6a (construction scope) |
| `Structural_Concrete_Rates.csv` | 15 items: concrete, formwork, rebar, structural steel, foundations | 6a (DEL-02-04, DEL-04-03) |
| `Building_Envelope_Rates.csv` | 15 items: wall/roof panels, cladding, insulation, glazing, doors, hardware | 6a (DEL-02-04, DEL-04-01) |
| `Mechanical_System_Rates.csv` | 14 items: HVAC/plumbing/fire protection $/sf, exhaust, equipment | 6a (DEL-02-05, DEL-04-04) |
| `Electrical_System_Rates.csv` | 14 items: power/lighting/telecom $/sf, fire alarm, PA, solar-ready | 6a (DEL-02-06, DEL-04-04) |
| `Earthwork_Civil_Rates.csv` | 11 items: clearing, excavation, fill, compaction, drainage, survey | 6a (DEL-03-02) |
| `Paving_Surfacing_Rates.csv` | 9 items: asphalt (heavy/light duty), aggregate, concrete aprons, curbs | 6a (DEL-03-03) |
| `Underground_Utility_Rates.csv` | 12 items: water, sewer, gas, power, telecom; municipal tie-in allowances | 6a (DEL-03-04) |
| `Equipment_Pricing.csv` | 15 items: overhead doors, generator, lockers, breathing air, sumps, etc. | 6a (PKG-002, PKG-004) |
| `Optional_Items_Pricing.csv` | 18 items: wash bay, yard lights, access control, cameras, signage, appliances, FF&E | 6a (PKG-005) |
| `Parametric_Building_Rates.csv` | 9 items: pre-engineered building $/sf, institutional $/sf, site $/sf, interior fit-up | All three (parametric validation) |
| `Fees_Permits_Insurance.csv` | 19 items: bonds, insurance, permits, utility connections, environmental fees | All three executions |
| `Professional_Design_Fees.csv` | 8 items: A/E design fee percentages by discipline | 6a (design fee allocation) |
| `Proposal_Level_of_Effort.csv` | Hours per deliverable per role (6a management + 6b full + 6c full) | 6a (PKG-001), 6b (all), 6c (all) |
| `Assumed_Project_Parameters.csv` | 29 parameters: areas, quantities, durations, rough financial estimates | All three executions |

---

## PS-ID Cross-Reference: Execution 6a

| 6a PS-ID | Source Needed | File(s) | Key Items |
|----------|--------------|---------|-----------|
| **PS-01** | DB internal staff rate table | `Professional_Staff_Rates.csv` | All R-xx roles; see also `Proposal_Level_of_Effort.csv` for 6a PKG-001 hours |
| **PS-02** | Assumed project duration | `Assumed_Project_Parameters.csv` | PP-01 (18 months construction), PP-02 (4 months design), PP-03 (22 months total) |
| **PS-03** | Structural steel/concrete unit rates | `Structural_Concrete_Rates.csv` | SC-01 through SC-15 |
| **PS-04** | Pre-engineered metal building pricing (60x100 cold storage) | `Parametric_Building_Rates.csv` | PB-01 ($28-35/sf shell), PB-02 ($42-55/sf turnkey) |
| **PS-05** | Building envelope systems pricing | `Building_Envelope_Rates.csv` | BE-01 through BE-15 |
| **PS-06** | Mechanical system rates | `Mechanical_System_Rates.csv` | MS-01 through MS-14 |
| **PS-07** | Electrical system rates | `Electrical_System_Rates.csv` | ES-01 through ES-14 |
| **PS-08** | Earthwork unit rates | `Earthwork_Civil_Rates.csv` | EC-01 through EC-11 |
| **PS-09** | Paving unit rates | `Paving_Surfacing_Rates.csv` | PS-01 through PS-09 (note: file uses PS prefix for paving items) |
| **PS-10** | Underground utility rates | `Underground_Utility_Rates.csv` | UU-01 through UU-12; UU-12 is the DEC-004 combined tie-in allowance |
| **PS-11** | Overhead door vendor quotes | `Equipment_Pricing.csv` | EQ-01 (car-wash grade, 8 units), EQ-02 (standard grade, 2 units) |
| **PS-12** | Diesel generator vendor quote | `Equipment_Pricing.csv` | EQ-04 (complete system $120k-180k) |
| **PS-13** | Vehicle exhaust extraction pricing | `Mechanical_System_Rates.csv` | MS-06 ($22k-28k per apparatus bay), MS-07 ($8k-14k per shop bay) |
| **PS-14** | Bunker gear locker pricing | `Equipment_Pricing.csv` | EQ-06 ($1800-2500 each, 40 units) |
| **PS-15** | PW locker pricing | `Equipment_Pricing.csv` | EQ-07 ($800-1200 each, 40 units) |
| **PS-16** | Breathing air compressor system | `Equipment_Pricing.csv` | EQ-08 ($45k-65k system) |
| **PS-17** | Bay sump assemblies | `Equipment_Pricing.csv` | EQ-10 ($3500-5500 each, 8 units); also MS-10 |
| **PS-18** | Permit fee schedule | `Fees_Permits_Insurance.csv` | FP-06 through FP-10 (building, dev, electrical, plumbing, gas permits) |
| **PS-19** | Environmental consultant fees | `Fees_Permits_Insurance.csv` | FP-16, FP-17, FP-18 (AEPA, environmental consulting, ESC plan) |
| **PS-20** | Cold storage foundation options | `Structural_Concrete_Rates.csv` | SC-12 (spread footings), SC-13 (strip footings), SC-14 (screw piles) |
| **PS-21** | Wash bay equipment | `Optional_Items_Pricing.csv` | OPT-01 through OPT-03 |
| **PS-22** | Yard lighting unit rate | `Optional_Items_Pricing.csv` | OPT-04 ($6500-9000 per unit), OPT-05 (conduit run) |
| **PS-23** | Access control system | `Optional_Items_Pricing.csv` | OPT-06 ($35k-55k for 10-zone), OPT-07 (per additional zone) |
| **PS-24** | Security camera system + monitoring | `Optional_Items_Pricing.csv` | OPT-08 ($40k-60k system), OPT-09 ($3600-7200/yr monitoring) |
| **PS-25** | Signage + branding | `Optional_Items_Pricing.csv` | OPT-10 (non-illuminated), OPT-11 (illuminated) — **BLOCKED: Town branding guidelines PENDING** |
| **PS-26** | Appliance pricing | `Optional_Items_Pricing.csv` | OPT-12 through OPT-17 (individual items + installation) |

---

## PS-ID Cross-Reference: Execution 6b

| 6b PS-ID | Source Needed | File(s) | Key Items |
|----------|--------------|---------|-----------|
| **PS-01** | Proposal production staff rate table | `Professional_Staff_Rates.csv` | All R-xx roles applicable to proposal production |
| **PS-02** | Production hours per deliverable | `Proposal_Level_of_Effort.csv` | Filter: Execution=6b; 38 deliverables x roles |
| **PS-03** | Proposal preparation timeline | `Assumed_Project_Parameters.csv` | PP-04 (6 weeks) |
| **PS-04** | Construction pricing for Schedule A/B | All construction rate files + `Parametric_Building_Rates.csv` | Full 6a-equivalent pricing library needed for DEL-01-04/05 construction content |
| **PS-05** | CCIP insurance premium rate | `Fees_Permits_Insurance.csv` | FP-03 (1.5-2.5% of construction value) |
| **PS-06** | Bond premium rate | `Fees_Permits_Insurance.csv` | FP-01 (performance 1.5%) + FP-02 (L&M 1.0%) |
| **PS-07** | Surety broker fee | `Fees_Permits_Insurance.csv` | FP-19 ($2000-5000 lump sum) |
| **PS-08** | Legal review hourly rate | `Professional_Staff_Rates.csv` | R-25 ($300/hr) |
| **PS-09** | CAD/BIM software costs | N/A | Assumed embedded in hourly rates (R-06); if separate, estimate $500-1000/month |
| **PS-10** | Scheduling software costs | N/A | Assumed embedded in hourly rate (R-17); if separate, estimate $200-400/month |
| **PS-11** | 3D rendering costs | N/A | Optional; if included, estimate 16-24 hours of R-06 CAD Tech time |
| **PS-12** | Printing/reproduction costs | N/A | Digital submission per RFP; negligible cost |

---

## PS-ID Cross-Reference: Execution 6c

| 6c PS-ID | Source Needed | File(s) | Key Items |
|----------|--------------|---------|-----------|
| **PS-01** | Proposal production staff rate table | `Professional_Staff_Rates.csv` | Same as 6b PS-01 |
| **PS-02** | Production hours per deliverable | `Proposal_Level_of_Effort.csv` | Filter: Execution=6c; 21 deliverables x roles |
| **PS-03** | Proposal preparation timeline | `Assumed_Project_Parameters.csv` | PP-04 (6 weeks) |
| **PS-04** | Construction pricing for Schedule A/B | All construction rate files + `Parametric_Building_Rates.csv` | Same as 6b PS-04; DEL-05-01/05-02 need full construction pricing |
| **PS-05** | Bond premium rate | `Fees_Permits_Insurance.csv` | FP-01 + FP-02 |
| **PS-06** | Insurance approach | `Fees_Permits_Insurance.csv` | FP-03 (CCIP), FP-04 (builder's risk), FP-05 (CGL) |
| **PS-07** | Surety broker fee | `Fees_Permits_Insurance.csv` | FP-19 |
| **PS-08** | Legal review hourly rate | `Professional_Staff_Rates.csv` | R-25 |
| **PS-09** | FF&E treatment decision (OI-004) | `Optional_Items_Pricing.csv` | OPT-18 ($20,000 fixed); **BLOCKING: OI-004 must be resolved before PKG-02 runs** |
| **PS-10** | CAD/BIM software costs | N/A | Assumed embedded in hourly rates |
| **PS-11** | Scheduling software costs | N/A | Assumed embedded in hourly rates |
| **PS-12** | 3D rendering costs | N/A | Optional |

---

## ESTIMATING Agent Instructions

When consuming these files, the ESTIMATING agent should:

1. **Load the applicable rate file(s)** based on the INIT-TASK brief's `PRICE_SOURCES` paths
2. **Match line items to rates** using ItemID references in the `SourceRef` column of Detail.csv
3. **Use `RecommendedRate`** as the point estimate; record `RateMin` and `RateMax` in risk analysis
4. **Flag `Confidence=LOW` items** in QA_Report.md for future vendor quote replacement
5. **Record `Basis` values** in Detail.csv Method column (PARAMETRIC, MARKET, or ALLOWANCE)
6. **For proposal production deliverables (6b/6c):** multiply `EstimatedHours` from LOE matrix by `HourlyRate_CAD` from staff rates; sum across roles per deliverable
7. **For construction deliverables (6a):** apply unit rates to quantities derived from deliverable documents and `Assumed_Project_Parameters.csv`
8. **Where parametric gaps exist:** use `Parametric_Building_Rates.csv` $/sf rates as a cross-check or fallback; flag in Decision_Log.md as "PARAMETRIC_FALLBACK"

### Gaps Requiring Parametric Estimation or Future Quotes

The following items have no pricing data and should be estimated parametrically by the ESTIMATING agent or flagged as TBD:

| Gap | Workaround |
|-----|-----------|
| Town of Penhold specific fee schedules (permits, utility connections) | Use Alberta municipal averages from `Fees_Permits_Insurance.csv` |
| Town branding guidelines (for signage option) | Carry as allowance per OPT-10/OPT-11 ranges |
| Actual vendor quotes for generator, breathing air, overhead doors | Use parametric ranges from `Equipment_Pricing.csv`; flag for future quote |
| Exact building dimensions (fire bay sizes, office areas) | Use `Assumed_Project_Parameters.csv` PP-05 through PP-08; refine when concept drawings available |
| Number of parking stalls, yard light poles | Use assumed quantities PP-19, PP-20; refine when site plan available |
| Utility tie-in allowance value (DEC-004) | Use UU-12 recommended $35,000; **Owner must confirm** |
| CCIP insurance actual premium | Use FP-03 percentage (2.0% recommended) until actual quote |
| 72-hour generator runtime confirmation | Assumed per PP-26; **Owner must confirm** |

---

## Document Control

| Field | Value |
|-------|-------|
| Document | PRICE_SOURCES Index |
| Version | DRAFT v0.1 |
| Prepared by | [Human operator] with HELP_HUMAN agent support |
| Date | 2026-02-18 |
| Status | DRAFT — Parametric estimates; no vendor quotes obtained |
| Shared across | execution-6a, execution-6b, execution-6c |

---

**END OF DOCUMENT**
