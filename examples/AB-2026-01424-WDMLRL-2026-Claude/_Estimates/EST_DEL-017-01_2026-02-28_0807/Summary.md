# Summary — EST_DEL-017-01_2026-02-28_0807

## Basis of Estimate

| Field | Value |
|-------|-------|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Rounding | NONE |
| Scope | DEL-017-01 — Kitchenette Renovation |
| Package | PKG-017 — Existing Building Renovation (Old North Shop) |
| PreviousSnapshot | EST_DEL-017-01_2026-02-27_0730 (41,901.44 CAD; 2 TBDs) |

## Totals by CBS

| CBS | Amount (CAD) | Line Count | % of Total |
|-----|-------------|------------|------------|
| Management | 10,085.40 | 14 | 21.1% |
| Construction | 37,816.04 | 18 | 78.9% |
| **TOTAL** | **47,901.44** | **32** | **100.0%** |

## Totals by Package / Deliverable

| Package | Deliverable | Amount (CAD) |
|---------|-------------|-------------|
| PKG-017 | DEL-017-01 | 47,901.44 |

## Delta from Previous Snapshot

| Item | Previous (CAD) | Current (CAD) | Delta (CAD) | Notes |
|------|---------------|---------------|-------------|-------|
| L-019 Gas Fitting Rough-In | TBD | 2,500 | +2,500 | Resolved using MS-07 recommended rate |
| L-020 Mechanical/HVAC Rough-In | TBD | 3,500 | +3,500 | Resolved using MS-08 recommended rate |
| All other lines | 41,901.44 | 41,901.44 | 0 | Unchanged |
| **TOTAL** | **41,901.44** | **47,901.44** | **+6,000** | |

## Key Warnings and Coverage Gaps

1. **Appliance and cabinetry scope is TBD.** The Datasheet identifies appliances and cabinetry as TBD pending the design phase and Owner approval. Procurement responsibility is ambiguous (Lensing: E-001). The current estimate uses the IA-05 casework allowance (11,000 CAD) split 50/50 between cabinetry (L-026) and fixtures/appliances (L-027). If Owner-furnished appliances are excluded from the contractor scope, L-027 would be reduced. Conversely, if high-end or specialized appliances are specified, 5,500 CAD may be insufficient.

2. **Gas fitting and HVAC/kitchen ventilation are now priced but remain conditional.** L-019 (gas fitting, 2,500 CAD) and L-020 (HVAC/mechanical, 3,500 CAD) have been priced using recommended rates from Mechanical_System_Rates.csv (MS-07 and MS-08 respectively). These items remain conditional on the appliance schedule: if gas appliances are excluded, L-019 may be removed; if cooking appliances are excluded, L-020 may be removed. Both are LOW confidence.

3. **Plumbing and electrical scope are design-gated.** Plumbing rough-in (L-017, 2,784 CAD) and electrical rough-in (L-018, 2,880 CAD) are parametric estimates based on assumed trade hours (30 hr each). The actual scope is TBD pending IFC drawings from PKG-004 and PKG-006.

4. **No material-only rates available.** Labour rates from Construction_Labour_Rates.csv cover trade hours only. Material costs for plumbing fixtures, electrical fixtures, and appliances are embedded in the parametric allowances (IA-05, labour productivity assumptions). Actual material costs depend on the approved fixture and appliance schedule.

5. **Fire separation scope is conditional.** If the renovation penetrates fire-rated assemblies (Specification REQ-013), firestopping work would be required. This is not separately priced; it is assumed to be captured within substrate preparation (L-021) and is a LOW-cost item unless major fire-rated assemblies are affected.

6. **Accessibility requirements are TBD.** Specification REQ-014 identifies accessibility as conditional pending Owner/Architect determination. If barrier-free design is required, additional costs for accessible cabinetry, counter heights, and clearances may apply.

7. **Hazardous materials.** The hazmat assessment allowance (L-012, 2,500 CAD) covers testing only. If abatement is required (ACM or lead paint), additional cost would apply and is not included.

## Confidence Assessment

- **HIGH confidence items:** None at this scope level; all items are parametric estimates.
- **MEDIUM confidence items:** Professional staff costs (L-001 to L-006) -- hours from Level_of_Effort.csv, rates from Professional_Staff_Rates.csv. Area-based interior finishes (L-022 to L-025) -- rates from Interior_Architectural_Rates.csv; area from RFP (250 sqft = 23.2 m2). Demolition (L-015), substrate prep (L-021), and management/closeout activities (L-009, L-011, L-028 to L-032) with parametric hours.
- **LOW confidence items:** Gas fitting (L-019), HVAC/mechanical (L-020) -- newly priced from Mechanical_System_Rates.csv but conditional on design. Cabinetry/fixtures (L-026, L-027), plumbing rough-in (L-017), electrical rough-in (L-018), hazmat assessment (L-012), waste disposal (L-016), utility verification (L-008), conditions survey (L-007) -- parametric estimates with significant scope uncertainty pending design.
