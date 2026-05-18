# QA Report — EST_DEL-02-01_2026-02-18_2000

**RUN_STATUS: OK**

---

## Schema Validity (Detail.csv)

| Check | Result |
|---|---|
| All required columns present | PASS (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid | PASS (all 4 rows = RATE_TABLE; valid enum) |
| Allowance/parametric convention | N/A (no ALLOWANCE or PARAMETRIC method rows) |
| Amount = Qty x UnitRate | PASS (L-001: 40x145=5800; L-002: 24x120=2880; L-003: 60x95=5700; L-004: 8x175=1400) |
| Currency consistent | PASS (all rows = CAD) |
| WBS IDs valid vs decomposition | PASS (PKG-002 and DEL-02-01 confirmed in decomposition v2.3) |

---

## Coverage

| Measure | Value |
|---|---|
| Deliverables in scope | 1 (DEL-02-01) |
| Deliverables covered (at least 1 priced line) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items produced | 4 |
| Line items with TBD amounts | 0 |

---

## Provenance Completeness

| Measure | Value |
|---|---|
| Total priced rows | 4 |
| Rows with SourceRef (non-TBD) | 4 (100%) |
| Rows with `location TBD` | 0 |
| Top missing-source offenders | None |

---

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE declared | RATE_TABLE |
| Methods used in Detail.csv | RATE_TABLE (4/4 rows) |
| Mixed methods detected | NO |
| ALLOW_MIXED_METHODS setting | FALSE |
| Basis consistency | PASS |

---

## Blocker Summary (from Dependency Evidence)

| Blocker Type | Count | Impact on Estimate |
|---|---|---|
| Upstream interface dependencies (design data from DEL-02-02 through DEL-02-05) | 4 | No impact on cost estimate; these are execution sequencing dependencies, not pricing blockers |
| Upstream prerequisite documents (OSR, Functional Program) | 2 | No impact on cost estimate; these are execution prerequisites |
| Upstream constraint documents (Addendum 03) | 1 | No impact on cost estimate; program requirements are embedded in scope |
| Downstream handovers | 4 | No impact on cost estimate; information flows from DEL-02-01 to downstream deliverables |

No dependency-related pricing blockers identified.

---

## Arithmetic Verification

| CBS | Sum from Detail.csv | Sum in WBS_CBS_Matrix.csv | Match |
|---|---|---|---|
| LABOR-DESIGN | 5800 + 2880 = 8680 | 8680 | PASS |
| LABOR-PRODUCTION | 5700 | 5700 | PASS |
| LABOR-MGMT | 1400 | 1400 | PASS |
| TOTAL | 15780 | 15780 | PASS |

---

## Rounding Verification

All amounts are whole dollars (DOLLAR rounding applied). No sub-dollar amounts exist in source data (all products of integer hours and integer rates).

---

## Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (OK) |
| Basis-consistency checks pass | PASS |
| Provenance completeness reported and actionable | PASS (100%) |
| Scope coverage explicit | PASS (1/1 deliverables covered) |
| No writes outside _Estimates/ | PASS |

---

## What to Fix for a Cleaner Rerun

Nothing required. This is a clean run with no warnings, no TBDs, and full provenance coverage.

Optional improvements for future iterations:
- Replace MARKET-basis rates with firm-specific rate agreements (would increase confidence from MEDIUM to HIGH).
- Replace PARAMETRIC-basis hours with historical actuals from comparable past projects.
- Add explicit CBS codes from a project-standard CBS dictionary rather than derived LABOR-{Category} codes.
