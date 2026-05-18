# PRICE_SOURCES Index — Execution 6c
## Proposal Production Cost Estimating (Consolidated)

**Execution Root:** `test/execution-6c/`
**BOE:** `test/execution-6c/_Estimates/BASIS_OF_ESTIMATE.md`
**Currency:** CAD | **Base Year:** 2024 | **Region:** Alberta (Penhold/Red Deer)
**Prepared:** 2026-02-18
**Status:** DRAFT — Parametric and market-based estimates; no vendor quotes

---

## Data Quality Statement

All rates are **parametric estimates based on Alberta 2024 market data**. Professional hourly rates reflect typical Design-Build firm internal rates. Level-of-effort hours are planning estimates based on comparable proposal efforts for $15-20M municipal DB projects.

This execution uses a **consolidated** decomposition (21 deliverables vs 6b's 38). Consolidated deliverables have higher per-deliverable hours due to multi-discipline coordination overhead bundled within single deliverables.

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
| `Professional_Staff_Rates.csv` | 30 roles | All 21 deliverables — hourly rates for proposal production roles |
| `Level_of_Effort.csv` | 65 rows | All 21 deliverables — hours per role per deliverable |
| `Assumed_Project_Parameters.csv` | 29 params | PP-04 (proposal timeline), PP-05-08 (areas for scope calibration) |
| `Fees_Permits_Insurance.csv` | 19 items | DEL-01-03 (bond/insurance premiums) |

### Construction pricing files (for Schedule A/B content in DEL-05-01, DEL-05-02)

These files provide the construction pricing that gets embedded IN the Schedule A and Schedule B forms.

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
| `Optional_Items_Pricing.csv` | 18 items | Schedule A/B optional items (Options 1-6); OPT-18 = FF&E per OI-004 |
| `Interior_Architectural_Rates.csv` | 25 items | Schedule A/B interior scope (partitions, ceilings, flooring, paint, accessibility, signage, millwork, specialties) |
| `Parametric_Building_Rates.csv` | 9 items | Parametric cross-check of Schedule A totals |
| `Construction_Labour_Rates.csv` | 15 trades | Schedule A/B labour rates |
| `Professional_Design_Fees.csv` | 8 items | Schedule A/B design fee line items |

---

## BOE PS-ID → File Mapping

| PS-ID | Source | File | Key Items |
|-------|--------|------|-----------|
| PS-01 | Proposal staff rate table | `Professional_Staff_Rates.csv` | All R-xx roles applicable to proposal production |
| PS-02 | Production hours per deliverable | `Level_of_Effort.csv` | 65 rows: 21 deliverables x applicable roles |
| PS-03 | Proposal preparation timeline | `Assumed_Project_Parameters.csv` | PP-04 (6 weeks) |
| PS-04 | Construction pricing for Schedule A/B | All construction rate files listed above | Full construction pricing library for DEL-05-01/05-02 content |
| PS-13 | Interior architectural | `Interior_Architectural_Rates.csv` | IA-01 through IA-25 (partitions, ceilings, flooring, paint, accessibility, signage, millwork, specialties) |
| PS-05 | Bond premium rate | `Fees_Permits_Insurance.csv` | FP-01 (performance 1.5%) + FP-02 (L&M 1.0%) |
| PS-06 | Insurance approach | `Fees_Permits_Insurance.csv` | FP-03 (CCIP 2.0%), FP-04 (builder's risk), FP-05 (CGL) |
| PS-07 | Surety broker fee | `Fees_Permits_Insurance.csv` | FP-19 ($2000-5000) |
| PS-08 | Legal review hourly rate | `Professional_Staff_Rates.csv` | R-25 ($300/hr) |
| PS-09 | FF&E treatment (OI-004) | `Optional_Items_Pricing.csv` | OPT-18 ($20,000 fixed) — **OI-004 must be resolved before PKG-02 runs** |
| PS-10 | CAD/BIM software costs | N/A | Embedded in R-06 hourly rate |
| PS-11 | Scheduling software costs | N/A | Embedded in R-17 hourly rate |
| PS-12 | 3D rendering costs | N/A | Optional: 16-24 hours of R-06 time |

---

## ESTIMATING Run Configuration

### DEL-to-PKG mapping (non-sequential numbering)

| Package | Deliverables |
|---------|-------------|
| PKG-01 (Compliance) | DEL-01-01, DEL-01-02, DEL-01-03 |
| PKG-02 (Financial) | DEL-05-01, DEL-05-02, DEL-05-03 |
| PKG-03 (Team) | DEL-07-01, DEL-07-02, DEL-07-03 |
| PKG-04 (Design) | DEL-02-01, DEL-02-02, DEL-02-03 |
| PKG-05 (Delivery Plan) | DEL-03-01, DEL-03-02 |
| PKG-06 (Construction) | DEL-04-01, DEL-04-02, DEL-04-03 |
| PKG-07 (Commissioning) | DEL-06-01 |
| PKG-08 (Schedule) | DEL-08-01 |
| PKG-09 (Due Diligence) | DEL-09-01, DEL-09-02 |

### For proposal production deliverables (18 of 21)

Most deliverables are pure proposal production cost:
`Cost = Σ (Hours_per_role × Hourly_rate_per_role)`

```
PRICE_SOURCES:
  - "{EXECUTION_ROOT}/_PriceSources/Professional_Staff_Rates.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Level_of_Effort.csv"
  - "{EXECUTION_ROOT}/_PriceSources/Assumed_Project_Parameters.csv"
```

### For DEL-05-01 (Schedule A) and DEL-05-02 (Schedule B)

Dual cost nature — production hours PLUS embedded construction pricing:

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

### Per-package source mapping

| Package | Primary PRICE_SOURCES |
|---------|----------------------|
| PKG-01 | Staff_Rates, LOE, Parameters, Fees (for DEL-01-03) |
| PKG-02 | Staff_Rates, LOE, Parameters, ALL construction files (for DEL-05-01/02 content), Fees |
| PKG-03 | Staff_Rates, LOE, Parameters |
| PKG-04 | Staff_Rates, LOE, Parameters |
| PKG-05 | Staff_Rates, LOE, Parameters |
| PKG-06 | Staff_Rates, LOE, Parameters |
| PKG-07 | Staff_Rates, LOE, Parameters |
| PKG-08 | Staff_Rates, LOE, Parameters |
| PKG-09 | Staff_Rates, LOE, Parameters |

---

## Consolidated Deliverable Notes

DEL-02-02 (Design Brief Narrative) is the **largest single production effort** in this decomposition — it covers 5 SOW items (SOW-010, 011, 013, 014, 015) requiring input from all 5 engineering disciplines plus building science. The Level_of_Effort.csv allocates **80 hours across 8 roles** for this deliverable. ESTIMATING should validate that the coordination overhead is adequately captured.

DEL-06-01 (Commissioning/Closeout/Warranty) and DEL-09-01 (Risk Register + QMP) are also consolidated deliverables with scope from multiple SOW items.

---

## Open Issues Affecting PRICE_SOURCES

| Issue | Impact | Status |
|-------|--------|--------|
| **OI-004: FF&E treatment** | Affects DEL-05-01/05-02 Schedule A/B line items | **OPEN — must resolve before PKG-02 runs** |
| OI-001: Intent to Propose | If submitted, add ~2-4 admin hours to PKG-01 | OPEN — low impact |

---

## Gaps Requiring Parametric Estimation

| Gap | ESTIMATING Workaround |
|-----|----------------------|
| Actual DB firm hourly rates | Use parametric Alberta market rates |
| Actual effort per deliverable | Use LOE estimates; flag as PARAMETRIC |
| CCIP insurance premium | Use FP-03 (2.0%) until actual quote |
| Bond premium rate | Use FP-01 + FP-02 (2.5% combined) |
| Construction pricing for Schedule A/B | Use construction rate files; flag as PARAMETRIC |
| OI-004 FF&E decision | Assume OPT-18 ($20k allowance); flag as PENDING |
| Reference document accessibility | Proceed with assumptions per decomposition procedure |

---

**END OF DOCUMENT**
