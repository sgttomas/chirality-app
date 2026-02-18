# Run Context — EST_DEL-02-01_2026-02-18_2100

## Run Identity

| Field | Value |
|---|---|
| RunID | EST_DEL-02-01_2026-02-18_2100 |
| AsOf | 2026-02-18T21:00:00-07:00 |
| PriorRunID | EST_DEL-02-01_2026-02-18_0800 |
| RevisionType | TBD resolution pass (ORCHESTRATOR-directed) |
| Agent | ESTIMATING (Type 2) — revision by ORCHESTRATOR |

## Brief Inputs (as provided)

| Parameter | Value |
|---|---|
| SCOPE | DEL-02-01 |
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/ |
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| OUTPUT_LABEL | DEL-02-01 |
| UPDATE_LATEST_POINTER | FALSE |
| ALLOW_MIXED_METHODS | FALSE |
| FALLBACK_POLICY | STRICT |
| ROUNDING | DOLLAR |

## Revision Notes

This snapshot revises EST_DEL-02-01_2026-02-18_0800 to resolve 7 TBD line items. The prior run could not price interior construction items because Interior_Architectural_Rates.csv (PS-27) was not yet available in the PRICE_SOURCES. PS-27 has since been added with 25 rate table items covering partitions, ceilings, flooring, paint, accessibility, signage, millwork, and specialties.

**Changes from prior run:**
- L-004: TBD → $30,225 (partitions; IA-01/02/04 blended at $93/m2 × 325 m2)
- L-005: TBD → $16,905 (floor finish; IA-08 at $35/m2 × 483 m2)
- L-006: TBD → $32,844 (ceiling; IA-05 at $68/m2 × 483 m2)
- L-007: TBD → $9,490 (accessibility; IA-15/16/17/18 composite)
- L-008: TBD → $11,520 (signage; IA-19/20/21 composite)
- L-009: TBD → $9,133 (paint; IA-12/13 blended at $14.05/m2 × 650 m2)
- L-010: TBD → $11,012 (design fees; DF-01 at 7% of $157,317 construction subtotal)
- No method changes: all lines remain RATE_TABLE (no mixed methods needed)
- Total changed from $47,200 → $168,329

## Resolved Inputs

| Parameter | Resolved Value |
|---|---|
| DECOMPOSITION_PATH | _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| DEPENDENCY_SOURCES | AUTO (DEL-02-01 Dependencies.csv, 23 rows) |
| PRICE_SOURCES | Building_Envelope_Rates.csv; Interior_Architectural_Rates.csv (NEW — PS-27); Professional_Design_Fees.csv; Construction_Labour_Rates.csv; Structural_Concrete_Rates.csv; Mechanical_System_Rates.csv; Electrical_System_Rates.csv; Equipment_Pricing.csv; Assumed_Project_Parameters.csv |

## Scope Resolution

| Field | Value |
|---|---|
| ScopeResolvedSummary | 1 deliverable in scope; 0 excluded; 0 blocked |
| DeliverableID | DEL-02-01 |
| PackageID | PKG-002 |
| Tier | T1 (foundational) |
| Substance | Design + Construction |

## Cost Ownership Boundaries

Carried forward from prior run. DEL-02-01 owns architectural design + interior construction (partitions, doors, finishes, accessibility, signage). Does not own structural/envelope (DEL-02-04), MEP (DEL-02-05/06/07), or bay functional fit-up (DEL-02-02/03).

## Area Breakdown (carried forward)

| Zone | Area (sf) | Area (m2) |
|---|---|---|
| Office/admin/shared spaces | 5,200 | 483 |
| Partition wall face area | 3,500 | 325 |
| Wall paint surface | 7,000 | 650 |

## CBS Mapping Rule

Carried forward from prior run: 3100=design fees, 3200=partitions, 3300=doors, 3400=finishes, 3500=accessibility, 3600=signage.
