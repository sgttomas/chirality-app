# QA Report -- EST_DEL-018-06_2026-03-26_1759

**RUN_STATUS: WARNINGS**

---

## Schema Validity

| Check | Result | Notes |
|---|---|---|
| Detail.csv parseable | PASS | 26 data rows, all required columns present |
| Detail.csv column completeness | PASS | All 14 required columns populated |
| Method enum validity | PASS | RATE_TABLE (14 rows), ALLOWANCE (12 rows) -- both valid enums |
| CBS codes valid | PASS | CBS-02, CBS-05, CBS-17, CBS-22, CBS-23, CBS-24, CBS-25, CBS-28, CBS-29 -- all in CBS_Taxonomy.csv |
| WBS_PackageID valid | PASS | PKG-018 confirmed in decomposition |
| WBS_DeliverableID valid | PASS | DEL-018-06 confirmed in decomposition |
| Allowance convention | PASS | All ALLOWANCE lines use Qty=1, Unit=LS, UnitRate=Amount |
| Amount = Qty x UnitRate | PASS | All 26 rows verified |

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables priced | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| SOW items covered | 4 (SOW-0080, SOW-0081, SOW-0082, SOW-0122) |
| Line items total | 26 |
| Line items with TBD amounts | 0 |

## Provenance Completeness

| Metric | Value |
|---|---|
| Rows with non-TBD SourceRef | 26 / 26 (100%) |
| Rows with `location TBD` | 0 |
| Rows citing ASSUMPTION | 12 / 26 (46%) |
| Top assumption-heavy items | DL-007 (gas tie-in), DL-008 (electrical tie-in), DL-009 (comms tie-in), DL-010 (pole relocation) |

## Basis-Consistency Check

| Check | Result | Notes |
|---|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE | Valid enum |
| Methods used vs basis | WARNING | 46% of lines use ALLOWANCE fallback (12 of 26 lines) |
| ALLOW_MIXED_METHODS | TRUE | Mixed methods permitted per brief |
| FALLBACK_POLICY | ALLOW_ALLOWANCE | Exercised for 12 lines where rate table evidence is insufficient |

**WARNING:** 46% of line items by count (but 75% by dollar value) use ALLOWANCE method rather than the primary RATE_TABLE basis. This is permitted by ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_ALLOWANCE, but indicates that the estimate's primary cost drivers lack rate table evidence. Obtaining provider quotes would materially improve estimate quality.

## Blocker Assessment (from Dependencies.csv)

| Blocker | Status | Impact on Estimate |
|---|---|---|
| DEP-018-06-007: Site Grading (DEL-018-02) | PENDING | Does not block cost estimate; affects construction sequencing |
| DEP-018-06-008: Civil Design IFC (PKG-005) | PENDING | Trench routing TBD -- 75m assumption carries risk |
| DEP-018-06-009: Electrical Calc Package (DEL-004-08) | PENDING | Electrical load sizing TBD -- affects service connection cost |
| DEP-018-06-010: Mechanical Calc Package (DEL-003-06) | PENDING | Gas load sizing TBD -- gas supply params now confirmed (Add. 3 Q8) |
| DEP-018-06-011: Safety Code Permits (DEL-009-03) | PENDING | Does not block cost estimate; affects construction sequencing |
| DEP-018-06-012: Utility Providers | PENDING | Provider quotes needed for SOW-0080, SOW-0081, SOW-0082, SOW-0122 |

**Blocker count impacting estimate accuracy:** 3 (civil routing TBD, electrical load TBD, provider quotes TBD)

## Confidence Assessment

| Confidence Level | Lines | Dollar Value | % of Total |
|---|---|---|---|
| MED | 14 | $61,100.20 | 31% |
| LOW | 12 | $139,000.00 | 69% |
| HIGH | 0 | $0 | 0% |

**WARNING:** 69% of the estimate value is LOW confidence. The primary LOW-confidence items are the four utility connection/relocation allowances ($133,000 combined) and the underground gas piping proxy rate ($9,750).

## Change vs Prior Snapshot

| Change | Description |
|---|---|
| New scope SOW-0122 | Electrical pole/transformer relocation (Add. 3, Q7) -- +$55,000 allowance + $2,240 support labour |
| Management hours increase | +6 hrs across CPM, Supt, HSE for SOW-0122 coordination |
| Commissioning increase | +$1,500 for pole relocation verification |
| Documentation increase | +$1,000 for expanded as-built scope |
| Gas params confirmed | 2" PVC, 50 PSI (Add. 3, Q8) -- no material cost change but reduced uncertainty |
| Total delta | +$60,620.00 (+43.5%) |
| Method change | Prior: PARAMETRIC; Current: RATE_TABLE + ALLOWANCE (per brief) |

## What to Fix for a Cleaner Rerun

1. **Obtain utility provider quotes** for electrical service (SOW-0081), gas service (SOW-0080), and especially electrical pole/transformer relocation (SOW-0122). These four items represent $133,000 (66% of total) at LOW confidence.
2. **Confirm trench distance** from civil design (PKG-005 IFC). The 75m assumption affects $27,375 of earthwork and underground utility costs.
3. **Resolve transformer ownership** -- customer-owned vs utility-owned has a $30,000-$80,000 cost impact.
4. **Confirm number of poles** affected by SOW-0122 relocation to narrow the $35,000-$85,000 range.
5. **Update Level_of_Effort.csv** to include SOW-0122 management hours natively.
6. **Add contingency line item** once scope uncertainty is reduced.
