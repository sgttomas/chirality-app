# Estimate Summary — EST_DEL-001-10_2026-02-27_0600

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method** | Level-of-Effort (hours) x Professional Staff Rates |
| **Currency** | CAD |
| **Scope** | DEL-001-10 — Old North Shop Renovation Plans |
| **Package** | PKG-001 — Architectural Design |
| **Deliverable Type** | Drawing Set |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE (not exercised; all lines are PARAMETRIC) |

## Estimate Total

| | Value |
|---|---|
| **Total Estimated Cost** | **$19,200.00 CAD** |
| **Total Hours** | **130 hrs** |
| **Priced Line Items** | 5 of 5 (100%) |
| **TBD Items** | 0 |

## Totals by CBS

| CBS | Amount (CAD) | Hours | Line Count |
|---|---|---|---|
| Design-Management | $1,530.00 | 10 | 2 |
| Design-Architecture | $17,670.00 | 120 | 3 |
| **TOTAL** | **$19,200.00** | **130** | **5** |

## Totals by Role

| RoleID | Role | Rate (CAD/hr) | Hours | Amount (CAD) | % of Total |
|---|---|---|---|---|---|
| R-01 | Project Manager | $165.00 | 6 | $990.00 | 5.2% |
| R-08 | Cost Estimator | $135.00 | 4 | $540.00 | 2.8% |
| R-11 | Senior Architect | $180.00 | 54 | $9,720.00 | 50.6% |
| R-12 | Architect | $135.00 | 42 | $5,670.00 | 29.5% |
| R-13 | BIM Technician | $95.00 | 24 | $2,280.00 | 11.9% |
| | **TOTAL** | | **130** | **$19,200.00** | **100.0%** |

## Scope Coverage

- **Deliverables in scope:** 1 (DEL-001-10)
- **SOW items covered by deliverable:** SOW-0070 (Kitchenette renovation), SOW-0071 (Mezzanine renovation), SOW-0072 (Washroom renovation), SOW-0073 (Locker/change room), SOW-0074 (Washroom urinal expansion)
- **Documents read:** 4 of 4 (Datasheet.md, Specification.md, Guidance.md, Procedure.md) -- all present
- **Items extracted in Items.csv:** 12 (5 priced labor items + 7 scope-descriptive items included in labor hours)

## Key Warnings and Coverage Gaps

1. **Renovation scope is design-only.** This estimate covers the professional design services (architectural drawing production) for the Old North Shop renovation plans. It does NOT include construction costs for executing the renovation work (SOW-0070 through SOW-0074), which are covered by PKG-017 deliverables.

2. **Existing conditions uncertainty.** The Old North Shop dimensions are derived from Appendix B conceptual drawings and are approximate (105 ft x 40 ft, ~4,200 sqft). Actual dimensions are TBD pending field survey. If existing conditions are significantly different from the conceptual plan, the LOE estimate may require adjustment.

3. **No construction cost cross-check for renovation scope.** The Parametric_Building_Rates.csv provides rates for new construction ($285/sf) but does not include a renovation-specific rate. The renovation construction cost is not estimated in this snapshot.

4. **Discipline coordination effort is embedded.** The hours for discipline coordination (REQ-009) are included in the PM and architect hours but not separately broken out. If coordination effort is higher than anticipated (e.g., due to mezzanine structural complexities or plumbing rework), additional hours may be required.

5. **Code compliance confirmation pending.** The governing Alberta Building Code edition is ASSUMED to be NBC 2019 Alberta Edition. If a different edition applies or if accessibility requirements are triggered, the design effort may increase.

## Cross-Check

- LOE-based estimate for DEL-001-10: **$19,200 CAD** (130 hours)
- Fee-based cross-check (4.5% architecture fee on $3,705,000 construction value / 11 PKG-001 deliverables): ~$15,157 CAD per deliverable (simple average)
- The LOE estimate is ~27% above the simple average fee share, which is reasonable given renovation plans require field survey and existing conditions assessment not typical for new-build drawing sets.
