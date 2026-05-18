# QA Report -- EST_DEL-04-04_2026-02-18_1500

## RUN_STATUS: OK

Totals are meaningful; no critical input gaps. All line items priced from rate table evidence with confirmed area parameter.

---

## 1. Schema Validity (Detail.csv)

| Check | Result |
|---|---|
| Detail.csv exists | PASS |
| All required columns present (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (RATE_TABLE) | PASS |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount) | N/A (no ALLOWANCE or PARAMETRIC lines) |
| Amount = Qty x UnitRate | PASS (L-0404-01: 6000 x 6 = 36000; L-0404-02: 6000 x 3 = 18000) |
| Currency consistent | PASS (all CAD) |
| Rounding = DOLLAR | PASS (all amounts are whole dollars) |

## 2. Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-04-04) |
| Deliverables covered (at least 1 priced line) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items total | 2 |
| Lines with TBD Amount | 0 |

## 3. Provenance Completeness

| Metric | Value |
|---|---|
| Total priced lines | 2 |
| Lines with explicit SourceRef | 2 (100%) |
| Lines with "location TBD" | 0 (0%) |
| Top missing-source offenders | None |

## 4. Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Methods used in Detail.csv | RATE_TABLE (2/2 lines) |
| Mixed methods present | NO |
| ALLOW_MIXED_METHODS setting | FALSE |
| Consistency | PASS (100% RATE_TABLE) |

## 5. Dependency / Blocker Assessment

| Metric | Value |
|---|---|
| Dependency rows loaded | 9 |
| Execution prerequisites (upstream) | 4 (DEP-04-04-004 through DEP-04-04-007) |
| Unresolved blockers to estimating | 0 |
| Notes | All dependencies are design/execution-phase prerequisites (building geometry, door schedule, floor system, climate data). None block rate-table-based estimating at this stage since we are using area-based parametric rates that do not require detailed design resolution. |

## 6. Scope Boundary Validation

| Check | Result |
|---|---|
| Building shell costs excluded | PASS (not priced) |
| Door/opener hardware costs excluded | PASS (only electrical feeds priced via ES-12) |
| Foundation/floor costs excluded | PASS (not priced) |
| Site utility service TO building excluded | PASS (only service entry from wall to panel included in ES-12) |
| Building pad preparation excluded | PASS (not priced) |
| Concrete aprons excluded | PASS (not priced) |

## 7. Risks / Sensitivities

- **Ventilation approach sensitivity:** MS-13 ($3/sf) assumes passive/low-energy ventilation (ridge vents, gable fans). If climate analysis (DEP-04-04-007) or AHJ requirements demand active mechanical ventilation, costs could increase to $5-8/sf range. Potential impact: +$12,000 to +$30,000.
- **Rate range sensitivity:** ES-12 ranges $5-8/sf (recommended $6). Using min/max: electrical range $30,000-$48,000. MS-13 ranges $2-4/sf (recommended $3). Using min/max: ventilation range $12,000-$24,000. Total range: $42,000-$72,000 (recommended: $54,000).

## 8. What to Fix for a Cleaner Rerun

- No critical fixes needed. Run status is OK.
- Optional improvement: if detailed design produces a specific lighting fixture count or ventilation equipment list, a bottom-up estimate could replace the area-based rates for higher confidence.
