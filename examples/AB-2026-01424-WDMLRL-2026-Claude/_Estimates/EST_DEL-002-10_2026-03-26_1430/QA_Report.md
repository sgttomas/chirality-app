# QA Report -- EST_DEL-002-10_2026-03-26_1430

**RUN_STATUS: WARNINGS**

---

## Schema Validity (Detail.csv)

| Check | Result |
|---|---|
| All required columns present | PASS (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid | PASS (RATE_TABLE: 4 priced + 9 trace; ALLOWANCE: 8 priced + 4 trace) |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS (all ALLOWANCE lines use Qty=1, Unit=LS, UnitRate=Amount) |
| All amounts computed correctly | PASS (verified: Qty x UnitRate = Amount for all priced lines) |
| Grand total reconciles | PASS (sum of priced lines = $22,460 CAD) |

---

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered | 1 (DEL-002-10) |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Structural subsystems traced | 9 of 9 (including new Interior Precast Walls) |
| Procedural activities traced | 4 of 4 |
| Priced line items | 12 |
| Scope trace lines ($0) | 13 |
| Total line items | 25 |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Priced rows with non-TBD SourceRef | 12 of 12 (100%) |
| Scope trace rows with non-TBD SourceRef | 13 of 13 (100%) |
| **Overall provenance completeness** | **100%** |
| Top missing-source offenders | None |

---

## Basis-Consistency Checks

| Check | Result | Notes |
|---|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE | Valid enum value |
| ALLOW_MIXED_METHODS | TRUE | Mixed methods authorized |
| Method mix | RATE_TABLE (59.4%) + ALLOWANCE (40.6%) | Consistent with ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_ALLOWANCE |
| RATE_TABLE lines use rates from PS-STAFF | PASS | R-01: $165, R-08: $135, R-13: $95, R-14: $170 -- all match Professional_Staff_Rates.csv |
| RATE_TABLE lines use hours from PS-LOE | PASS | R-01: 6h, R-08: 4h, R-13: 24h, R-14: 56h -- all match Level_of_Effort.csv DEL-002-10 rows |
| ALLOWANCE lines have documented basis | PASS | All reference specific addenda and assumption IDs |

---

## Blocker Assessment (from Dependencies.csv)

| DependencyID | Target | Status | Estimate Impact |
|---|---|---|---|
| DEP-002-10-E01 | DEL-008-01 (Geotech Report) | PENDING | BLOCKING for final foundation calcs; not blocking for this estimate (normal ground conditions basis) |
| DEP-002-10-E02 | DEL-016-01 (Crane Procurement) | PENDING | ADVISORY; conservative parameters used; corbel design allowance included |
| DEP-002-10-E03 | DEL-001-01 (Preliminary Architectural Design) | PENDING | ADVISORY; App B dimensions sufficient for estimation |

**Active blockers affecting estimate quality:** 0 (all upstream dependencies are non-blocking for estimate purposes; flagged for downstream reconciliation).

---

## Warnings

| # | Warning | Severity | Actionable Fix |
|---|---|---|---|
| W-001 | 40.6% of estimate value ($9,130) is ALLOWANCE with LOW confidence (+/-30-50%) | MEDIUM | Update LOE.csv with post-SCA-001 hour allocations; re-run as full RATE_TABLE |
| W-002 | LOE.csv baseline hours are pre-SCA-001 (monolithic concrete assumption) | MEDIUM | Refresh LOE.csv to reflect hybrid precast+steel structural system |
| W-003 | Foundation reconciliation hours not separately quantified | LOW | Add explicit reconciliation allowance when geotech report timeline is known |
| W-004 | Crane reconciliation hours not separately quantified beyond corbel design | LOW | Add explicit reconciliation allowance when crane procurement timeline is known |
| W-005 | Prior estimate used PARAMETRIC basis; this run uses RATE_TABLE + ALLOWANCE | INFO | Basis change is intentional per run brief; delta is driven by scope, not method change |

---

## What to Fix for a Cleaner Rerun

1. **Update Level_of_Effort.csv** with post-SCA-001 hour allocations reflecting the hybrid precast concrete walls + steel roof structural system. This would eliminate the ALLOWANCE supplement and produce a pure RATE_TABLE estimate.
2. **Obtain precast supplier connection design scope** to refine the connection design hours allowance (currently 12 hrs Structural Engineer).
3. **Confirm crane manufacturer data availability timeline** to determine whether crane reconciliation hours should be estimated now.
4. **Resolve DEL-008-01 (geotech)** to determine foundation reconciliation effort.
