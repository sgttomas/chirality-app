# Estimate Summary — EST_DEL-015-03_2026-02-27_0148

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Scope | DEL-015-03 — Receptacle Installation |
| Package | PKG-015 — Electrical & Low-Voltage Installation |

**Methodology:** Parametric estimation using Electrical_System_Rates.csv (ES-04 for 50A welding receptacles at $950/EA installed), Construction_Labour_Rates.csv (T-04 Electrician at $96.00/hr fully burdened), Professional_Staff_Rates.csv + Level_of_Effort.csv (staff hours and rates for management/oversight roles), and parametric unit-rate models for receptacle devices and rough-in materials not explicitly covered by price sources.

---

## Totals by Package / Deliverable

| WBS Package | WBS Deliverable | Total (CAD) |
|---|---|---|
| PKG-015 | DEL-015-03 | **$36,363.00** |

---

## Totals by Cost Breakdown Structure (CBS)

| CBS Category | Amount (CAD) | % of Total | Line Count |
|---|---|---|---|
| Material — Devices | $9,670.00 | 26.6% | 7 |
| Labour — Trade | $14,304.00 | 39.3% | 5 |
| Labour — Professional | $6,790.00 | 18.7% | 7 |
| Material — Rough-In | $3,720.00 | 10.2% | 5 |
| Permits | $1,500.00 | 4.1% | 1 |
| Material — Accessories | $379.00 | 1.0% | 3 |
| **TOTAL** | **$36,363.00** | **100.0%** | **28** |

---

## Key Cost Drivers

1. **Electrician trade labour ($14,304)** — 39.3% of total. Driven by 144 hours of electrician time across rough-in (80 hrs), device installation (40 hrs), testing (16 hrs), and closeout (8 hrs) at $96/hr fully burdened. The 50A welding receptacle labour is included in the ES-04 installed rate.
2. **Material — Devices ($9,670)** — 26.6% of total. The six 50A welding-grade receptacles at $950/EA installed (ES-04) account for $5,700, being the largest single material cost driver. Circuit breakers (45 EA at $45 avg) add $2,025.
3. **Professional staff ($6,790)** — 18.7% of total. Management and oversight roles per Level_of_Effort.csv allocations. Design coordination (IFC review, RFI resolution) adds $1,200.

---

## Key Warnings and Coverage Gaps

| Warning ID | Description | Impact |
|---|---|---|
| W-001 | Receptacle quantities are approximate (from conceptual drawing); IFC drawings not yet issued | Quantities could change +/-20% at IFC stage; cost impact ~$5,000-8,000 range |
| W-002 | NEMA configurations for 20A/240V, 30A/240V, 50A/240V are TBD | Device procurement cannot be finalized; cost impact likely minor if configuration changes |
| W-003 | Construction parameters (installation method, wiring system, GFCI/AFCI zones) TBD pending IFC | Could affect rough-in material and labour quantities |
| W-004 | Trade labour hours parametrically estimated (not from LoE source) | LoE.csv only covers professional staff for DEL-015-03; trade hours are PARAMETRIC estimates |
| W-005 | No explicit rate source for 15A/20A/30A receptacle devices or rough-in materials | Parametric rates used with MED confidence; actual supplier quotes may differ |
| W-006 | Permit fee is a parametric allowance ($1,500) | Actual Alberta Safety Codes permit fee depends on scope valuation and municipality |

---

## Scope Coverage

- **Deliverables in scope:** 1 (DEL-015-03)
- **Documents read:** 4 of 4 (Datasheet, Specification, Guidance, Procedure) — all present
- **Items extracted:** 28 line items in Items.csv
- **Items priced:** 28 of 28 (100%)
- **Items with TBD amounts:** 0
- **Provenance completeness:** 100% — all lines have SourceRef entries
