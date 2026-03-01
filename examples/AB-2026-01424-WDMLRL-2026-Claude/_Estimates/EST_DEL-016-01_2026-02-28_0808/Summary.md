# Estimate Summary — EST_DEL-016-01_2026-02-28_0808

## Basis of Estimate

| Field | Value |
|-------|-------|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **Methods Used** | PARAMETRIC (16 lines), ALLOWANCE (3 lines — crane equipment supply+install from EQ-01, anti-collision system from EQ-04), TBD (0 lines) |
| **Currency** | CAD |
| **Scope** | DEL-016-01 — Two 5-Tonne Overhead Cranes (Procurement + Installation) |
| **Package** | PKG-016 — Crane & Lifting Equipment |
| **PriorSnapshot** | EST_DEL-016-01_2026-02-27_0133 |

## Totals by Cost Breakdown Structure (CBS)

| CBS | Amount (CAD) | Line Count | Notes |
|-----|-------------|------------|-------|
| EQUIP | $405,000.00 | 3 | 2 cranes at $190,000/each (ALLOWANCE, LOW confidence); anti-collision system $25,000 (ALLOWANCE, LOW confidence) |
| CONST_LABOUR | $12,084.80 | 5 | Ironworker, labourer, electrician installation hours |
| COMMISSION | $15,000.00 | 4 | Functional test, load test, AHJ inspection, owner demo |
| PROF_STAFF | $12,590.00 | 9 | PM, CPM, Site Super, QA/QC, HSE, estimator, procurement, drawings, closeout |
| FREIGHT | $12,000.00 | 1 | Freight allowance to rural Alberta site |
| **TOTAL** | **$456,674.80** | **22** | **All lines priced (0 TBD)** |

## Totals by Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Amount (CAD) |
|---------------|-------------------|-------------|
| PKG-016 | DEL-016-01 | $456,674.80 |

## Change from Prior Snapshot

| Metric | Prior (0133) | Current (0808) | Delta |
|--------|-------------|----------------|-------|
| Total | $431,674.80 | $456,674.80 | +$25,000.00 |
| TBD lines | 1 | 0 | -1 |
| Priced lines | 21 | 22 | +1 |

**Change detail:** DL-021 (anti-collision system) resolved from TBD to $25,000 ALLOWANCE based on Equipment_Pricing.csv EQ-04.

## Key Warnings and Coverage Gaps

1. **W-001 — Equipment pricing is LOW confidence.** The EQ-01 allowance ($190,000/each) has a range of $120,000 to $280,000 per unit. This means the equipment cost alone could range from $240,000 to $560,000 for both cranes. The total estimate is highly sensitive to the crane procurement price.

2. **W-002 — Multiple TBD design parameters.** Crane span, hook height, runway length, voltage/amperage, duty class, and applicable standards are all TBD per the Datasheet. The equipment pricing is based on a generic 5-tonne overhead crane allowance, not a specified model. Pricing accuracy will improve once these parameters are resolved and actual quotes are obtained.

3. **W-003 — Construction labour hours are estimated parametrically.** The installation labour (ironworker, labourer, electrician) hours are assumptions (ASM-003 through ASM-005) based on typical industrial crane installation scope. Actual hours will depend on crane model, site access, and installation conditions.

4. **W-004 — Anti-collision system is conditional.** DL-021 is now priced at $25,000 (ALLOWANCE, LOW confidence) based on EQ-04, but this item may not be required if independent runways are confirmed. The EQ-04 range is $15,000-$35,000.

5. **W-005 — EQ-01 is a combined supply+install allowance.** The Equipment_Pricing.csv EQ-01 item is described as "supply + install." There is potential double-counting with the separate construction labour lines (DL-003 through DL-007) which price installation labour independently. DECISION DEC-002 documents the rationale: the EQ-01 allowance is treated as primarily equipment supply with basic factory-standard installation, while the separate labour lines cover the site-specific rigging, assembly, and electrical work that may or may not be included in a supplier's "install" price. This is flagged for review.

6. **W-006 — No contingency or escalation applied.** This estimate does not include contingency, management reserve, or cost escalation. These are typically applied at a higher rollup level.

## Coverage Summary

| Metric | Value |
|--------|-------|
| Deliverables in scope | 1 |
| Items extracted (Items.csv) | 16 |
| Detail lines (Detail.csv) | 22 |
| Priced lines | 22 (100%) |
| TBD lines | 0 (0%) |
| Provenance completeness | 100% (all lines have SourceRef) |
| Documents read | 5 of 5 (Datasheet, Specification, Guidance, Procedure, _CONTEXT.md) |
