# Estimate Summary — DEL-01-03 Health & Safety (Prime Contractor) Plan

## Revision

| Field | Value |
|---|---|
| This Run | EST_DEL-01-03_2026-02-18_2100 |
| Prior Run | EST_DEL-01-03_2026-02-18_1720 |
| Revision Type | TBD resolution pass |
| Changes | 2 TBD lines resolved (L-0103-003 training → $4,500; L-0103-004 PPE/signage → $3,500) |

## Basis of Estimate Used

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| ROUNDING | DOLLAR |
| FALLBACK_POLICY | STRICT (with ALLOWANCE override for TBD resolution) |
| ALLOW_MIXED_METHODS | TRUE (authorized for TBD resolution) |

## Totals by CBS

| CBS | Description | Amount (CAD) | Status |
|---|---|---|---|
| CBS-LABOUR-SAFETY | Safety Officer labour | $6,600 | Priced (RATE_TABLE) |
| CBS-LABOUR-ADMIN | Admin / Document Control labour | $640 | Priced (RATE_TABLE) |
| CBS-TRAINING | Training costs | $4,500 | Priced (ALLOWANCE) |
| CBS-SUPPLIES | PPE / signage supplies | $3,500 | Priced (ALLOWANCE) |
| **TOTAL** | | **$15,240** | **Complete** |

## Totals by Deliverable

| DeliverableID | Name | PackageID | Amount (CAD) | TBD Lines | Total Lines |
|---|---|---|---|---|---|
| DEL-01-03 | Health & Safety (Prime Contractor) Plan | PKG-001 | $15,240 | 0 | 4 |

## Key Warnings

1. **Two ALLOWANCE lines at LOW confidence.** L-0103-003 ($4,500 training) and L-0103-004 ($3,500 PPE/signage) are parametric allowances, not sourced from rate tables or vendor quotes. Actual costs depend on workforce size, training requirements, and PPE standards.

2. **LOE_BASIS_MISMATCH (carried forward).** Hour quantities in Level_of_Effort.csv are marked as PARAMETRIC basis. This run treats them as quantity inputs priced at RATE_TABLE rates. See Decision_Log DEC-EST-001.

3. **Mixed methods now present.** L-0103-001/002 are RATE_TABLE; L-0103-003/004 are ALLOWANCE.
