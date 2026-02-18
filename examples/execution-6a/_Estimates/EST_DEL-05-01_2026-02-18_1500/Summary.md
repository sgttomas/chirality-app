# Estimate Summary -- DEL-05-01 (Option -- Built-in Wash Bay)

## Identification

| Field | Value |
|---|---|
| **Snapshot** | EST_DEL-05-01_2026-02-18_1500 |
| **Deliverable** | DEL-05-01_Optional-Wash-Bay |
| **Package** | PKG-005 (Optional Priced Items & Owner-Elected Additions) |
| **Scope Item** | SOW-0500 |
| **Option Type** | OPTIONAL PRICED ITEM -- separately priced from base scope |

## Basis of Estimate Used

| Field | Value |
|---|---|
| **Declared Basis** | QUOTE |
| **Actual Method Used** | ALLOWANCE (fallback) |
| **Fallback Reason** | No vendor quote exists; FALLBACK_POLICY=ALLOW_ALLOWANCE; ALLOW_MIXED_METHODS=TRUE |
| **Pricing Source** | Optional_Items_Pricing.csv (rows OPT-01, OPT-02, OPT-03) |
| **Confidence** | LOW (all items) |
| **Action Required** | Replace all allowance figures with vendor quotes before contract execution |

## Total by Deliverable

| WBS_DeliverableID | Currency | Amount | Line Count | Notes |
|---|---|---|---|---|
| DEL-05-01 | CAD | **$123,000** | 3 | All ALLOWANCE; all LOW confidence |

## Total by CBS

| CBS | Description | Currency | Amount |
|---|---|---|---|
| CBS-0500-EQUIP | Wash bay equipment/system (complete) | CAD | $95,000 |
| CBS-0500-PLMB | Plumbing/drainage modifications | CAD | $16,000 |
| CBS-0500-ENVR | Environmental compliance (effluent treatment) | CAD | $12,000 |
| | **TOTAL** | **CAD** | **$123,000** |

## Range Analysis

| Scenario | Amount (CAD) | Notes |
|---|---|---|
| **Low (all minimums)** | $95,000 | OPT-01 $75k + OPT-02 $12k + OPT-03 $8k |
| **Recommended (carried)** | $123,000 | OPT-01 $95k + OPT-02 $16k + OPT-03 $12k |
| **High (all maximums)** | $158,000 | OPT-01 $120k + OPT-02 $20k + OPT-03 $18k |

The spread between low and high is $63,000 (66% of the recommended figure), reflecting the LOW confidence level across all items.

## Cost Ownership Boundaries (Double-Count Prevention)

This estimate includes ONLY the following wash bay-specific costs:

| Included in DEL-05-01 | NOT included (owned by other deliverables) |
|---|---|
| Wash bay equipment + containment + dedicated plumbing | Base building bay sumps (DEL-02-05) |
| Wash bay drainage modifications beyond base rough-in | Base building mechanical rough-in (DEL-02-05) |
| Wash bay HVAC modifications | PW bay functional fit-up (DEL-02-03) |
| Wash bay environmental compliance (effluent treatment) | Structural modifications (DEL-02-04) |

## Key Warnings

1. **No vendor quote exists.** All figures are budget allowances requiring replacement with competitive quotes.
2. **Environmental requirements unresolved.** AEP/Town regulatory guidance not yet obtained (DEP-05-01-E04). Effluent treatment cost could materially exceed the carried allowance.
3. **PW bay layout prerequisite.** DEL-02-03 bay configuration must be confirmed before wash bay concept is finalized (DEP-05-01-E01).
4. **LOW confidence across all items.** The $123,000 figure should be presented to the Owner as a preliminary budget estimate, not a firm price.

## Blockers (from dependency evidence)

- 3 critical blockers identified (PW bay layout, AEP requirements, fleet vehicle dimensions)
- 6 execution-phase interfaces identified (all TBD status)
- See Blockers.md for details
