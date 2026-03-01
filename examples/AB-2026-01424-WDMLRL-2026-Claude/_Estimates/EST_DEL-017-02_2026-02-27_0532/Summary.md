# Summary — EST_DEL-017-02_2026-02-27_0532

## Basis of Estimate

| Field | Value |
|-------|-------|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Rounding | NONE |
| Scope | DEL-017-02 — Old North Shop Mezzanine Renovation |
| Package | PKG-017 — Existing Building Renovation (Old North Shop) |

## Totals by CBS

| CBS | Amount (CAD) | Line Count | % of Total |
|-----|-------------|------------|------------|
| Management | 9,845.40 | 13 | 13.1% |
| Design | 20,290.00 | 3 | 27.1% |
| Construction | 44,767.50 | 14 | 59.8% |
| **TOTAL** | **74,902.90** | **30** | **100.0%** |

## Totals by Package / Deliverable

| Package | Deliverable | Amount (CAD) |
|---------|-------------|-------------|
| PKG-017 | DEL-017-02 | 74,902.90 |

## Key Warnings and Coverage Gaps

1. **Mezzanine area is TBD.** The Datasheet states the mezzanine footprint is pending field measurement. An assumed area of 30 m2 (~323 sqft) was used for all area-based items (flooring, partitions, ceilings, paint, demolition). This is the single largest quantity driver for construction costs. If the actual area differs, costs will change proportionally for 5 line items totalling 8,896.50 CAD.

2. **Structural condition unknown.** Structural repairs (L-014, 7,500 CAD) are a parametric allowance. Actual cost could range from nil (if structure is sound) to significantly higher (if major remediation is needed). The Guidance document identifies a contingency pathway where the mezzanine may not be economically repairable.

3. **Stair/railing scope uncertain.** The stair and railing allowance (L-016, 6,000 CAD) is conditional on the structural/code assessment. If full replacement is required, this amount may be insufficient.

4. **Electrical scope is assumed.** No explicit SOW item exists for mezzanine electrical. The estimate includes 70 hr of electrician time (rough-in + completion) as parametric estimate. Actual scope depends on design.

5. **Hazardous materials.** The hazmat assessment allowance (L-012, 2,500 CAD) covers testing only. If abatement is required (ACM or lead paint), additional cost would apply and is not included.

6. **No material-only rates** are available in the price sources for structural steel, electrical fixtures, stair components, or plumbing fixtures. Labour rates from Construction_Labour_Rates.csv were used with parametric productivity assumptions. Material costs are embedded in the parametric rates where applicable (Interior_Architectural_Rates includes supply + install) or included as parametric allowances.

7. **Design costs are significant (27.1%).** This reflects the design-build nature of the project where the contractor provides full design services. The renovation design package (L-009, 12,810 CAD) is the single largest line item.

## Confidence Assessment

- **HIGH confidence items:** Professional staff costs (L-001 to L-006) — hours from Level_of_Effort.csv, rates from Professional_Staff_Rates.csv.
- **MEDIUM confidence items:** Area-based interior finishes (L-017 to L-021) — rates from Interior_Architectural_Rates.csv; area is assumed.
- **LOW confidence items:** Structural repairs (L-014), stair/railing (L-016), hazmat (L-012), design package (L-009), electrical (L-015, L-018) — parametric estimates with significant scope uncertainty.
