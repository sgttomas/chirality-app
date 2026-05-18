# Summary — EST_DEL-008-03_2026-02-27_0630

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Scope | DEL-008-03 Construction Survey |
| Package | PKG-008 Geotechnical Investigation & Surveying |

The estimate is based on parametric hour estimates for professional staff roles priced at rates from Professional_Staff_Rates.csv. Project Manager (6 hr) and Cost Estimator (4 hr) hours are sourced from Level_of_Effort.csv. Surveyor (R-21) hours (178 hr total) are parametrically estimated because the LOE source shows "TBD" for this role on DEL-008-03; the FALLBACK_POLICY=ALLOW_PARAMETRIC authorizes this approach.

## Totals

### By Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | CBS | Amount (CAD) | Line Count |
|---|---|---|---|---|
| PKG-008 | DEL-008-03 | Professional Services | 26,450 | 23 |
| **Total** | | | **26,450** | **23** |

### By Role

| Role | RoleID | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| Surveyor | R-21 | 178 | 140 | 24,920 |
| Project Manager | R-01 | 6 | 165 | 990 |
| Cost Estimator | R-08 | 4 | 135 | 540 |
| **Total** | | **188** | | **26,450** |

### By Phase (Surveyor hours only)

| Phase | Description | Hours | Amount (CAD) |
|---|---|---|---|
| Phase A | Mobilization and Planning (Steps A1-A4) | 30 | 4,200 |
| Phase B | Pre-Construction Layout (Steps B2-B8) | 54 | 7,560 |
| Phase C | Construction Phase Verification (Steps C1-C7) | 68 | 9,520 |
| Phase D | Documentation and Handoff (Steps D1-D3) | 24 | 3,360 |
| — | OH&S Compliance | 2 | 280 |
| **Surveyor Total** | | **178** | **24,920** |

**Note:** Phase subtotals include only Surveyor (R-21) hours. PM and CE hours are project-level overhead allocated across all phases.

## Key Warnings and Coverage Gaps

1. **Surveyor hours are fully parametric.** The Level_of_Effort.csv source provides "TBD" for Surveyor hours on DEL-008-03. All 178 Surveyor hours are agent-estimated based on scope analysis of the four deliverable documents. Confidence is MEDIUM overall (LOW for progress surveys due to undefined frequency).

2. **Progress survey frequency is TBD.** ITEM-016 / DL-016 estimates 8 visits x 4 hr = 32 hr at LOW confidence. Actual effort depends on the construction schedule and Construction Manager requirements. This is the single largest uncertainty in the estimate.

3. **No equipment costs included.** The estimate covers professional staff time only. Survey equipment (total station, GNSS, levels) is assumed included in the Surveyor's hourly rate. If equipment is priced separately, the estimate will understate total cost.

4. **No travel/mobilization costs.** Per-diem, vehicle, and travel costs for multiple site visits over the construction period are not included. The Surveyor rate ($140/hr) is assumed to be all-inclusive. If separate mobilization charges apply, the estimate will understate total cost.

5. **No field technician / survey assistant hours.** The rate table includes only the Surveyor (R-21) role. If a two-person survey crew is required (standard for total station work), the actual field cost may be higher.

6. **Foundation re-staking risk.** RFP §4.8.2 creates a risk that foundation staking must be performed twice (preliminary layout + final form staking after geotech-informed design). The estimate includes an allowance for this (ITEM-004 includes rough + final staking), but the allowance is parametric and may be insufficient if significant design changes occur.

7. **Construction Survey Summary Report (ITEM-019) is conditional.** Whether the report is required is TBD per Procedure Step D2. If not required, 8 hours ($1,120) could be removed.
