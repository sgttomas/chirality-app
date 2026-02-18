# Estimate Summary -- DEL-01-03 Health & Safety (Prime Contractor) Plan

## Basis of Estimate Used

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| ROUNDING | DOLLAR |
| FALLBACK_POLICY | STRICT |
| ALLOW_MIXED_METHODS | FALSE |

Pricing is derived from Professional_Staff_Rates.csv (hourly rates) applied to Level_of_Effort.csv (estimated hours). Non-labour cost drivers identified in the brief (training costs, PPE/signage supplies) have no available pricing source and are carried as TBD under the STRICT fallback policy.

## Totals by CBS

| CBS | Description | Amount (CAD) | Status |
|---|---|---|---|
| CBS-LABOUR-SAFETY | Safety Officer labour | $6,600 | Priced |
| CBS-LABOUR-ADMIN | Admin / Document Control labour | $640 | Priced |
| CBS-TRAINING | Training costs | TBD | No source |
| CBS-SUPPLIES | PPE / signage supplies | TBD | No source |
| **TOTAL (priced lines)** | | **$7,240** | **Partial** |

## Totals by Deliverable

| DeliverableID | Name | PackageID | Priced Amount (CAD) | TBD Lines | Total Lines |
|---|---|---|---|---|---|
| DEL-01-03 | Health & Safety (Prime Contractor) Plan | PKG-001 | $7,240 | 2 | 4 |

## Key Warnings

1. **PARTIAL_PRICING**: 2 of 4 line items are TBD (training costs and PPE/signage supplies). The $7,240 total represents labour costs only and understates the full deliverable cost.
2. **LOE_BASIS_MISMATCH**: Hour quantities in Level_of_Effort.csv are marked as PARAMETRIC basis. This run treats them as quantity inputs priced at RATE_TABLE rates. See Decision_Log.md DEC-EST-001.
3. **CBS codes are agent-derived**: No formal CBS was provided in the decomposition. CBS labels used here are project-specific and should be aligned with any formal CBS if one is established.

## Blockers

No pricing blockers prevent this run from completing. The TBD items are due to missing pricing sources, not missing scope information. If training and PPE/signage supply cost data is provided, a rerun will produce a complete estimate.

## Dependency Notes (from Dependencies.csv)

- DEP-0103-E005: DEL-01-06 (Site Supervision, Logistics & Housekeeping) is a prerequisite for the construction-phase H&S Plan. This is a sequencing dependency and does not block cost estimation.
- DEP-0103-E004: Alberta OHS Act/Regulations/Code is an external regulatory input. Compliance is assumed; no cost impact modeled separately.
