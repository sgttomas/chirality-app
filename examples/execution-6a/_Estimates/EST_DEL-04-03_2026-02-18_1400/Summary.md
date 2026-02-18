# Estimate Summary: DEL-04-03 -- Cold Storage Floor & Foundation (DB Proposed)

## Run Identity

| Field | Value |
|---|---|
| **Snapshot** | EST_DEL-04-03_2026-02-18_1400 |
| **Deliverable** | DEL-04-03 Cold Storage -- Floor & Foundation (DB Proposed) |
| **Package** | PKG-004 Cold Storage Building (Unheated, 60'x100') |
| **Basis of Estimate** | RATE_TABLE |
| **Currency** | CAD |
| **Rounding** | DOLLAR |

## Basis of Estimate Used

- **Method:** RATE_TABLE -- all line items priced from unit rates in Structural_Concrete_Rates.csv and derived rates documented in Decision_Log.md.
- **Design Selection:** Screw piles (foundation) + grade-supported concrete slab (floor) + concrete aprons at all 4 door openings.
- **Rationale:** Screw piles selected per geotechnical report recommendation ("ideal" for this site); concrete slab selected for durability and operational suitability. Per DEC-002 (DB proposes one floor solution) and DEC-003 (DB proposes most cost-effective code-compliant foundation).
- **Scope Boundaries:** Foundation + floor only. Building shell (DEL-04-01), building pad preparation (DEL-03-02), and electrical/ventilation (DEL-04-04) are excluded per cost ownership rules.

## Totals by CBS

| CBS | Description | Amount (CAD) | Line Count |
|---|---|---|---|
| 02-Sitework | Granular base + vapour barrier | $11,140 | 2 |
| 03-Concrete | Grade beams + floor slab + aprons + rebar | $75,514 | 4 |
| 05-Metals | Screw piles + anchor bolts | $63,600 | 2 |
| 31-Earthwork | Subgrade preparation | $6,684 | 1 |
| **TOTAL** | **DEL-04-03 Floor & Foundation** | **$156,938** | **10** |

## Totals by Deliverable

| WBS_PackageID | WBS_DeliverableID | Amount (CAD) |
|---|---|---|
| PKG-004 | DEL-04-03 | $156,938 |

## Parametric Cross-Check

| Check | Value | Source | Result |
|---|---|---|---|
| Cold storage turnkey PEMB (complete) | $48/sf x 6,000 sf = $288,000 | PB-02 (Parametric_Building_Rates.csv) | PB-02 includes shell + foundation + floor + doors + basic electrical + ventilation |
| This estimate (foundation + floor only) | $156,938 | Detail.csv | 54.5% of PB-02 turnkey rate |
| Implied remaining (shell + doors + elec + vent) | $131,062 | Derived (PB-02 minus this estimate) | Reasonable -- shell is typically 35-45% of total for a PEMB |

The parametric cross-check shows this estimate at approximately 55% of the complete turnkey rate. This is higher than a typical foundation/floor allocation (usually 30-40% of total) but is defensible given: (a) screw piles add cost vs. shallow foundations, (b) full concrete slab is the higher-cost floor option, and (c) the sulphate-resistant concrete mix increases unit rates. The estimate appears reasonable but is at the upper bound of expected allocation -- the screw pile count (20) and grade beam scope (80 lm) are the primary cost drivers that should be validated by structural engineering.

## Key Warnings

1. **Pile count is estimated (ASM-001, ASM-002).** 20 screw piles assumes a typical PEMB perimeter column layout at 10-12 ft spacing. Actual pile count depends on structural engineering and PEMB manufacturer column layout. Sensitivity: +/- 4 piles = +/- $12,000.
2. **Grade beam quantity is estimated (ASM-006).** 80 lm of grade beam is a judgment-based estimate for pile-cap-to-pile-cap beams. Actual length depends on structural design. Sensitivity: +/- 20 lm = +/- $4,400.
3. **Floor live load not confirmed (Datasheet [B-001]).** Slab thickness (150mm) may need to increase if heavy equipment loads exceed standard storage assumptions.
4. **Subgrade preparation and granular base rates are derived (ASM-007, ASM-008).** These rates are not direct line items in the rate tables; they are derived from the parametric site rate and typical cost breakdowns. See Decision_Log.md for derivation.

## Blockers

No blocking dependencies were identified for estimating purposes. All 12 dependency rows in Dependencies.csv are either anchor/traceability rows or interface/prerequisite rows for design execution (post-award), not for proposal-stage estimating.
