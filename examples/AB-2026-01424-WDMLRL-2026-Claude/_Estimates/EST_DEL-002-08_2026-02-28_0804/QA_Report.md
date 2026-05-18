# QA Report — EST_DEL-002-08_2026-02-28_0804

**RunID:** EST_DEL-002-08_2026-02-28_0804
**AsOf:** 2026-02-28T08:04:00-07:00

---

## RUN_STATUS: OK

All items priced. No blocking issues detected.

---

## 1. Schema Checks

| Check | Result | Details |
|---|---|---|
| Detail.csv column count | PASS | 15 columns present, matching expected schema (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Detail.csv row count | PASS | 6 data rows (LN-001 through LN-006) |
| Items.csv column count | PASS | 9 columns present, matching expected schema (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) |
| Items.csv row count | PASS | 6 data rows (ITM-001 through ITM-006) |
| LineID uniqueness | PASS | All 6 LineIDs are unique |
| ItemID uniqueness | PASS | All 6 ItemIDs are unique |
| LineID-to-ItemID mapping | PASS | Each LineID maps to a distinct ItemID (1:1) |
| Currency consistency | PASS | All lines report CAD |
| Method consistency | PASS | All lines report PARAMETRIC |
| WBS_PackageID consistency | PASS | All lines report PKG-002 |
| WBS_DeliverableID consistency | PASS | All lines report DEL-002-08 |

---

## 2. Provenance Completeness

| Check | Result | Details |
|---|---|---|
| SourceRef populated | PASS | All 6 lines have a non-empty SourceRef field |
| Rate traceability | PASS | LN-001 through LN-004 and LN-006 trace to Professional_Staff_Rates.csv with specific role codes (R-01, R-08, R-13, R-14) |
| Hours traceability | PASS | LN-001 through LN-004 trace to Level_of_Effort.csv with deliverable/role keys; LN-006 traces to Decision_Log DEC-R01 |
| Zero-cost line justification | PASS | LN-005 ($0.00) has a Notes field explaining that effort is captured within ITM-004 Structural Engineer hours |
| Source files exist | PASS | All 4 price source files listed in Run_Context.md are present in the PriceSources directory |

---

## 3. Pricing Coverage

| Check | Result | Details |
|---|---|---|
| Total items | 6 | LN-001 through LN-006 |
| Items priced (Amount > 0) | 5 | LN-001 ($990), LN-002 ($540), LN-003 ($3,420), LN-004 ($14,280), LN-006 ($1,360) |
| Items at zero (justified) | 1 | LN-005 ($0.00) — coordination effort embedded in LN-004; justified in Notes |
| Items TBD | 0 | None remaining |
| Pricing coverage | 100% | All items are priced or justified at zero |

---

## 4. Arithmetic Checks

| Check | Result | Details |
|---|---|---|
| LN-001: 6 x $165.00 = $990.00 | PASS | Matches Detail.csv Amount |
| LN-002: 4 x $135.00 = $540.00 | PASS | Matches Detail.csv Amount |
| LN-003: 36 x $95.00 = $3,420.00 | PASS | Matches Detail.csv Amount |
| LN-004: 84 x $170.00 = $14,280.00 | PASS | Matches Detail.csv Amount |
| LN-005: 1 x $0.00 = $0.00 | PASS | Matches Detail.csv Amount |
| LN-006: 8 x $170.00 = $1,360.00 | PASS | Matches Detail.csv Amount |
| Management subtotal: $990.00 + $540.00 = $1,530.00 | PASS | Matches Summary.md |
| Design subtotal: $3,420.00 + $14,280.00 + $0.00 + $1,360.00 = $19,060.00 | PASS | Matches Summary.md |
| Grand total: $1,530.00 + $19,060.00 = $20,590.00 | PASS | Matches Summary.md |

---

## 5. Cross-File Consistency

| Check | Result | Details |
|---|---|---|
| Detail.csv totals match Summary.md | PASS | Grand total $20,590.00 CAD consistent across both files |
| Items.csv count matches Detail.csv | PASS | 6 items in both files |
| Run_Context.md scope matches Detail.csv | PASS | Scope DEL-002-08 in PKG-002; all lines reference these WBS codes |
| Prior snapshot delta matches Summary.md | PASS | Delta of +$1,360.00 from prior snapshot ($19,230.00 to $20,590.00) consistent with LN-006 resolution |

---

## 6. Warnings and Observations

- **No blocking issues.**
- LN-005 and LN-006 carry LOW confidence; these should be revisited if scope details change.
- Peer review hours (LN-006, 8 hrs) are an assumption-level estimate (see Assumptions_Log ASM-001 and Decision_Log DEC-R01).
