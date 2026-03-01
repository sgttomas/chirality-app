# QA Report — EST_DEL-001-09_2026-02-27_0546

## RUN_STATUS: OK

---

## 1. Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows have valid PricingMode (UNIT_RATE or LUMP_SUM) | PASS |
| All rows trace to a SourceDoc and SourceSection | PASS |
| Row count | 10 items |

### Detail.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values are valid enum (QUOTE/RATE_TABLE/HISTORICAL/ALLOWANCE/PARAMETRIC) | PASS — all 5 lines are PARAMETRIC |
| Allowance/parametric convention respected | N/A — all lines are UNIT_RATE with hr quantities; convention applies to LS lines only |
| Row count | 5 priced lines |

### WBS_CBS_Matrix.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present | PASS |
| Totals reconcile with Detail.csv | PASS — $1,530 + $15,390 + $2,280 = $19,200 |

---

## 2. Quantity Takeoff Coverage

| Deliverable | Items Extracted | Documents Read | Missing Documents |
|---|---|---|---|
| DEL-001-09 | 10 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | None |

**Coverage assessment:** All four deliverable documents were read. 10 priceable items were extracted. 5 items (ITEM-001 through ITEM-005) represent direct staff-hour costs and are priced. 5 items (ITEM-006 through ITEM-010) represent activities that are subsumed within the LOE hours of the first 5 items and carry $0 additional cost — they are retained for scope traceability.

---

## 3. Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 10 |
| Items with priced Detail.csv lines | 5 (ITEM-001 through ITEM-005) |
| Items with $0 / subsumed cost (not TBD) | 5 (ITEM-006 through ITEM-010) |
| Items with TBD amount | 0 |
| **Pricing coverage** | **100%** (all items are either priced or explicitly documented as subsumed) |

---

## 4. Provenance Completeness

| Metric | Value |
|---|---|
| Detail.csv rows with non-TBD SourceRef | 5 of 5 (100%) |
| Detail.csv rows with `location TBD` | 0 |
| **Provenance completeness** | **100%** |

All 5 priced lines reference both the rate source (Professional_Staff_Rates.csv with row ID) and the LOE source (Level_of_Effort.csv with deliverable and role ID).

---

## 5. Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (5 of 5 lines) |
| Method mix consistent with basis? | PASS — 100% PARAMETRIC |
| FALLBACK_POLICY invoked? | No — all items had direct pricing evidence |
| ALLOW_MIXED_METHODS triggered? | No — single method used |

---

## 6. Scope Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-001-09) |
| Deliverables estimated | 1 (DEL-001-09) |
| SOW items covered by deliverable | SOW-0070, SOW-0071, SOW-0072 |
| Excluded from this estimate | Construction costs (PKG-017), MEP demolition design (PKG-003/004/006), structural demolition design (PKG-002) |

---

## 7. Warnings

| # | Severity | Warning | Recommended Action |
|---|---|---|---|
| W-001 | LOW | Mezzanine area (SOW-0071) is TBD — no measured area from sources | Confirm mezzanine area via field survey; reassess LOE if area is significantly larger than typical |
| W-002 | LOW | Washroom area (SOW-0072) is TBD — no measured area from sources | Confirm washroom area via field survey; reassess LOE if area is significantly larger than typical |
| W-003 | LOW | No as-built drawings confirmed for existing Old North Shop | If as-builts are unavailable, field survey effort may exceed LOE allocation |
| W-004 | LOW | Hazardous materials assessment not included in LOE | If hazmat design scope is required, add specialist hours |
| W-005 | LOW | P.Eng. stamp fee assumed included in Senior Architect rate | Confirm whether external P.Eng. co-stamp is required (CONF-001); if so, add cost |
| W-006 | LOW | No printing/reproduction costs included | Add if physical drawing sets required |

---

## 8. What to Fix for a Cleaner Rerun

1. **Obtain measured areas** for mezzanine (SOW-0071) and washroom (SOW-0072) from field survey to validate LOE allocation.
2. **Confirm P.Eng. stamp arrangement** (CONF-001) — if external P.Eng. is needed, add a line item.
3. **Confirm hazardous materials assessment requirement** — if required, add specialist hours to LOE.
4. **Add printing/reproduction costs** if applicable.
5. **Validate LOE hours** against firm historical data for similar renovation demolition plan drawing sets.

---

## 9. Operator Acceptance Checklist

| Check | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS — OK |
| Items.csv reviewed for completeness | 10 items extracted; 5 priced, 5 subsumed (all documented) |
| Basis-consistency checks pass | PASS — 100% PARAMETRIC |
| Provenance completeness reported | 100% |
| Scope coverage explicit | 1 of 1 deliverable; included/excluded clearly stated |
| No writes outside _Estimates/ | PASS |
