# QA Report -- EST_DEL-01-07_2026-02-18_1830

## RUN_STATUS: OK

All pricing inputs are available; all line items are priced with full provenance; no critical input gaps.

## Schema Validity (Detail.csv)

| Check | Result |
|---|---|
| All required columns present | PASS (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid | PASS (all 3 rows = RATE_TABLE) |
| Amount = Qty x UnitRate | PASS (L-0107-01: 120 x 140 = 16800; L-0107-02: 30 x 175 = 5250; L-0107-03: 20 x 80 = 1600) |
| Allowance/parametric convention | N/A (no ALLOWANCE or PARAMETRIC method rows) |
| Currency consistent | PASS (all rows = CAD) |
| Rounding applied | PASS (all amounts are whole dollars; ROUNDING=DOLLAR) |

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-01-07) |
| Deliverables with priced lines | 1 (DEL-01-07) |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items total | 3 |
| Total amount (CAD) | $23,650 |

## Provenance Completeness

| Metric | Value |
|---|---|
| Total priced rows | 3 |
| Rows with non-TBD SourceRef | 3 (100%) |
| Rows with TBD SourceRef | 0 (0%) |
| Provenance completeness | 100% |

No missing-source offenders.

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Methods used | RATE_TABLE (3/3 rows) |
| ALLOW_MIXED_METHODS | FALSE |
| Mixed method deviation | NONE -- PASS |
| FALLBACK_POLICY | STRICT |
| Fallback rows | 0 -- PASS |

## Blocker Assessment (from dependency evidence)

| Metric | Value |
|---|---|
| Total dependencies (Dependencies.csv) | 14 |
| ANCHOR edges | 6 |
| EXECUTION edges (upstream) | 7 |
| EXECUTION edges (downstream) | 1 |
| Unresolved blockers to estimating | 0 |

All upstream dependencies are informational for estimating purposes. None block the ability to price DEL-01-07 using rate-table inputs. System-specific commissioning costs (PKG-002 discipline outputs) are explicitly out of scope for this deliverable's estimate.

## Identified Gaps and Reviewer Actions

### Gap 1: Legal survey cost not captured (LOW severity)

DEL-01-07 scope includes SOW-0113 (certified as-built legal/topographical survey). The coordination labor to manage the survey is included in R-21 (Commissioning Lead) hours. However, the external surveyor fee is not captured in this rate-table estimate because no quote or allowance was provided in PRICE_SOURCES. If the survey cost should be carried under DEL-01-07, a QUOTE or ALLOWANCE line item would need to be added in a subsequent run.

### Gap 2: Confirm PKG-002 carries system-specific Cx costs (MEDIUM severity)

The cost ownership rules state that system-specific commissioning labor (mechanical balancing, electrical testing, controls commissioning) is in PKG-002 discipline deliverables. Reviewer should confirm those estimates exist and are complete to avoid a coverage gap between DEL-01-07 (coordination) and PKG-002 (execution).

### Gap 3: Rate confidence is MEDIUM (LOW severity)

All rates are MARKET-basis from Professional_Staff_Rates.csv. If contractual rates or negotiated rates become available, a re-run with updated PRICE_SOURCES would increase confidence.

## What to Fix for a Cleaner Re-run

1. **Add survey quote/allowance** to PRICE_SOURCES if legal survey cost should be carried in DEL-01-07.
2. **Confirm rate table** against contractual or negotiated rates when available.
3. **Validate hours** against historical commissioning/closeout effort for projects of comparable scope ($8.7M base construction value per PP-24).
