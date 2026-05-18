# QA Report

**Snapshot:** EST_DEL-03-01_2026-02-18_2000
**Date:** 2026-02-18

---

## RUN_STATUS: OK

Totals are meaningful; no critical input gaps. All pricing inputs (hours and rates) are sourced from provided files with full provenance.

---

## Schema Validity (Detail.csv)

| Check | Result |
|---|---|
| All required columns present | PASS (14/14 columns) |
| `Method` values valid | PASS (1 row: RATE_TABLE) |
| Allowance/parametric convention | N/A (no ALLOWANCE or PARAMETRIC method rows) |
| `Amount` = `Qty` x `UnitRate` | PASS (12 x 145 = 1,740) |
| Currency consistent | PASS (all CAD) |
| Rounding applied | PASS (DOLLAR; 1740 is whole dollar) |

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (priced) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items produced | 1 |

## Provenance Completeness

| Metric | Value |
|---|---|
| Total priced rows | 1 |
| Rows with non-TBD SourceRef | 1 |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Method values in Detail.csv | RATE_TABLE (1/1 rows) |
| Mixed methods detected | NO |
| ALLOW_MIXED_METHODS | FALSE |
| Consistency | **PASS** |

Note: The hours in Level_of_Effort.csv carry a `Basis=PARAMETRIC` label, indicating the hour quantities were derived parametrically. However, the pricing method used in this estimate is RATE_TABLE (hours x hourly rate from a rate table). This is consistent: the Level_of_Effort file provides the quantity input, and the rate table provides the unit rate. The `Method` column correctly reflects the pricing method (RATE_TABLE), not the quantity derivation method.

## Blocker Assessment (from Dependency Evidence)

| Metric | Value |
|---|---|
| Total dependencies loaded | 17 |
| Upstream prerequisites (EXECUTION class) | 1 (DEP-03-01-004: DEL-02-01 required) |
| Upstream constraints (documents/standards) | 4 (RFP 7.1.2, OSR, Addendum 03, Functional Program) |
| Upstream interfaces | 2 (Geotech report, DEL-04-01) |
| Downstream interfaces/handovers | 6 (DEL-03-02 through DEL-03-06, DEL-05-01, DEL-01-02) |
| Anchor dependencies | 3 (WBS node, SOW-0011, OBJ-004) |
| Dependencies blocking estimating | **0** (all pricing inputs available) |
| Dependencies blocking production | 1 (DEL-02-01 SatisfactionStatus=TBD) |

## What to Fix for a Cleaner Rerun

1. No material issues identified. This is a clean run.
2. If hour estimates in Level_of_Effort.csv are refined (e.g., based on actual concept package complexity), rerun to update totals.
3. If rate table is updated with firmer rates (currently MEDIUM confidence, MARKET basis), rerun to reflect.
