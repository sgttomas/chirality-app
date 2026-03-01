# Summary — EST_DEL-014-06_2026-02-27_0201

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Methods Used | PARAMETRIC (11 lines), RATE_TABLE (9 lines) |

This estimate uses parametric pricing for fixture materials and installation items (no fixture-specific quotes or rate tables available in PRICE_SOURCES), and rate-table pricing for plumber labour and professional staff LOE using Construction_Labour_Rates.csv and Professional_Staff_Rates.csv respectively.

## Totals by CBS

| CBS | Description | Amount (CAD) | Line Count |
|---|---|---|---|
| 14-PLUMB-FIXT | Fixture materials, equipment, and installation items | $10,520.00 | 9 |
| 14-PLUMB-LAB | Plumber trade labour (install, test, commissioning) | $3,340.80 | 3 |
| 14-MGMT | Management and oversight (PM, CPM, Site Sup, CE, QA/QC, HSE) | $5,590.00 | 6 |
| 14-PLUMB-ADMIN | Submittal preparation and review | $1,200.00 | 1 |
| 14-PLUMB-INSP | Safety Code inspection | $500.00 | 1 |
| **TOTAL** | **DEL-014-06 Plumbing Fixtures** | **$21,150.80** | **20** |

## Totals by Package / Deliverable

| Package | Deliverable | Amount (CAD) |
|---|---|---|
| PKG-014 | DEL-014-06 Plumbing Fixtures | $21,150.80 |

## Key Warnings and Coverage Gaps

### Warnings

1. **No fixture material pricing sources available.** All fixture material costs (water taps, pressure washer reel, industrial wash station, valves, drain assemblies, backflow devices, trim) are priced using PARAMETRIC estimates. These should be replaced with vendor quotes as design progresses and DEL-006-06 (Fixture Schedule) is produced.

2. **Conditional item included: Point-of-use water heater ($1,800).** This item is conditional on resolution of CONF-014-06-01 (hot water supply for wash station). If hot water is not required, remove DL-007 and reduce total by $1,800 to $19,350.80.

3. **Fixture specifications are TBD.** Numerous attributes (flow rates, operating pressures, material specifications, fixture models) are TBD pending DEL-006-06 Plumbing Fixture Schedule. Parametric estimates assume mid-range industrial-grade fixtures appropriate for a landfill maintenance shop.

4. **Backflow prevention devices are assumed required** for cistern-fed (non-municipal) water source. Quantity and type TBD per AHJ determination.

5. **Pressure washer system scope boundary.** EQ-02 in Equipment_Pricing.csv carries $11,000 for a full pressure washer system. DEL-014-06 scope includes only the retractable hose reel and water connection (not the pressure washer machine itself, per CONF-014-06-02). The $3,500 parametric estimate for the reel assembly is distinct from the full system allowance.

6. **Safety Code inspection fee is LOW confidence** -- actual fee depends on AHJ fee schedule which is not in PRICE_SOURCES.

### Coverage

| Metric | Value |
|---|---|
| Items extracted from documents | 20 |
| Items priced | 20 (100%) |
| Items with TBD amount | 0 |
| Items at LOW confidence | 2 (DL-007 conditional heater, DL-020 inspection fee) |
| Items at MED confidence | 18 |
| Provenance completeness | 100% (all lines have SourceRef) |
