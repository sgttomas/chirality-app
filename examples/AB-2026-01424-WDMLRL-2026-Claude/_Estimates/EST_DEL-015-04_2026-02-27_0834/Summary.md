# Estimate Summary — DEL-015-04 Equipment Power Circuits

**RunID:** EST_DEL-015-04_2026-02-27_0834
**Basis of Estimate:** PARAMETRIC
**Currency:** CAD
**RUN_STATUS:** WARNINGS

---

## Basis of Estimate Used

| Field | Value |
|---|---|
| Primary Method | PARAMETRIC |
| Fallback Policy | ALLOW_PARAMETRIC |
| Mixed Methods | TRUE — RATE_TABLE used for professional staff and construction labour where rate tables exist; PARAMETRIC used for equipment/material items lacking specific quotes |
| Price Sources | 6 CSV files (Professional_Staff_Rates, Level_of_Effort, Assumed_Project_Parameters, Electrical_System_Rates, Underground_Utility_Rates, Construction_Labour_Rates) |

---

## Total by Package / Deliverable

| Package | Deliverable | Total (CAD) |
|---|---|---|
| PKG-015 | DEL-015-04 (Equipment Power Circuits) | **74,364.00** |

---

## Total by CBS (Cost Breakdown Structure)

| CBS | Amount (CAD) | Line Count | Pct of Total |
|---|---|---|---|
| Electrical-Equipment | 54,650.00 | 17 | 73.5% |
| Construction-Labour | 14,124.00 | 2 | 19.0% |
| Professional-Staff | 5,590.00 | 6 | 7.5% |
| **TOTAL** | **74,364.00** | **25** | **100.0%** |

---

## Key Cost Drivers

1. **Overhead crane power circuits (L-001, L-002):** $17,000 combined (22.9% of total). These are the highest-value individual items and carry LOW confidence because crane manufacturer electrical requirements are TBD pending DEL-016-01 procurement. The conductor bar/festoon system pricing is a parametric allowance.
2. **Electrician labour (L-024):** $11,520 (15.5% of total). Parametric estimate of 120 hours at $96.00/hr fully burdened rate.
3. **Conduit/raceway (L-010):** $9,000 (12.1% of total). 120 m of conduit at $75/m parametric rate.
4. **Conductor wire (L-011):** $5,400 (7.3% of total). 120 m at $45/m average across mixed gauge sizes.

---

## Warnings and Coverage Gaps

| ID | Category | Description | Impact |
|---|---|---|---|
| W-001 | TBD Quantities | Crane circuit voltage and amperage are TBD pending manufacturer data (DEL-016-01) | Crane circuit costs (L-001, L-002) could vary significantly; LOW confidence |
| W-002 | TBD Quantities | Overhead door count assumed 4; actual count TBD per IFC architectural drawings | Door circuit cost (L-003) may change proportionally |
| W-003 | TBD Quantities | Exhaust fan count assumed 2; scope boundary with PKG-013 unresolved (CON-015-04-001) | Fan circuit cost (L-007) may change; scope boundary ruling required |
| W-004 | Missing BOM | No bill of materials exists for this deliverable; all material pricing is parametric | Material costs carry MED to LOW confidence |
| W-005 | Pricing Gaps | No specific rate for conductor bar/festoon systems, circuit breakers, motor disconnects, or conductor wire in provided price sources | Parametric benchmarks used; validation against quotes recommended |
| W-006 | Voltage TBD | Multiple circuit voltages are TBD (compressor, fire hose pump, pressure washer) | Conductor sizing and associated material costs may change with voltage confirmation |

---

## Scope Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-015-04) |
| Documents read | 4 of 4 (Datasheet, Specification, Guidance, Procedure) |
| Missing documents | 0 |
| Priceable items extracted | 25 |
| Items priced | 25 of 25 (100%) |
| Items with TBD Amount | 0 |
| Provenance completeness | 100% (all lines have SourceRef) |
