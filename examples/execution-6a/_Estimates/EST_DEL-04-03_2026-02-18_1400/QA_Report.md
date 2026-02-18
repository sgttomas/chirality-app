# QA Report

## RUN_STATUS: WARNINGS

Some totals exist but material assumptions remain regarding pile count, grade beam quantities, and derived rates for subgrade preparation, granular base, and vapour barrier. The estimate is directionally sound and suitable for proposal-stage budgeting, but quantities should be validated by structural engineering before use as a commitment basis.

---

## S1 -- Write Quarantine Respected

**PASS.** All files written under `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/EST_DEL-04-03_2026-02-18_1400/`. No files outside `_Estimates/` were created or modified.

## S2 -- Snapshot Created

**PASS.** Snapshot folder `EST_DEL-04-03_2026-02-18_1400` created under ESTIMATES_ROOT.

## S3 -- BASIS_OF_ESTIMATE Validated

**PASS.** `RATE_TABLE` is a valid enum value.

## S4 -- Required Artifacts Exist

**PASS.** All required files present:
- [x] Run_Context.md
- [x] Summary.md
- [x] QA_Report.md (this file)
- [x] Source_Index.md
- [x] Decision_Log.md
- [x] Assumptions_Log.md
- [x] WBS_CBS_Matrix.csv
- [x] Detail.csv (optional but produced)
- [x] Blockers.md (optional but produced)

## S5 -- Detail Schema Integrity

**PASS.**

| Check | Result |
|---|---|
| Detail.csv parseable | YES |
| All 14 required columns present | YES (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid | YES -- all 10 rows use `RATE_TABLE` |
| Allowance/parametric convention | N/A -- no ALLOWANCE or PARAMETRIC method rows |
| Line count | 10 rows |
| Currency consistent | YES -- all CAD |

## S6 -- Provenance Discipline

**PASS with notes.**

| Metric | Value |
|---|---|
| Total priced rows | 10 |
| Rows with direct rate table SourceRef | 7 (L-001, L-002, L-003, L-004, L-005, L-009, L-010) |
| Rows with derived rate + Decision_Log ref | 3 (L-006, L-007, L-008) |
| Rows with `location TBD` | 0 |
| Provenance completeness | 100% (all rows have a SourceRef) |

**Note on derived rates:** Three line items (L-006 subgrade prep, L-007 granular base, L-008 vapour barrier) use rates derived by the estimating agent because no direct rate table item exists. These are documented in Decision_Log.md (DEC-EST-007, DEC-EST-008, DEC-EST-009) with derivation rationale. The rates are reasonable for Alberta market conditions but are not sourced from the provided rate tables and therefore carry higher uncertainty.

### Top provenance concerns (ranked by cost impact):

1. **L-007 Granular base ($8,355):** Derived rate ($15/m2). Potential double-count risk with SC-03 "includes sub-base prep." If double-counted, total would decrease by ~$8,355.
2. **L-006 Subgrade prep ($6,684):** Derived rate ($12/m2). Reasonable but not directly supported by rate table.
3. **L-008 Vapour barrier ($2,785):** Derived rate ($5/m2). Low-cost item; minimal risk.

## S7 -- Status Reporting

**RUN_STATUS = WARNINGS**

Justification:
- Totals are meaningful ($156,938 CAD for DEL-04-03 floor + foundation).
- Parametric cross-check against PB-02 shows reasonable allocation (54.5% of turnkey PEMB rate).
- Material assumptions remain: pile count, grade beam quantity, floor live load, and 3 derived rates.
- No TBD amounts in Detail.csv -- all rows are priced.
- 12 assumptions documented in Assumptions_Log.md; all rated MED confidence.

## Basis-Consistency Check

**PASS.** All 10 line items use Method=RATE_TABLE, matching BASIS_OF_ESTIMATE=RATE_TABLE. ALLOW_MIXED_METHODS=FALSE is respected. No fallback methods were needed (FALLBACK_POLICY=STRICT).

## Coverage Check

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-04-03) |
| Deliverables with priced line items | 1 (DEL-04-03) |
| Deliverables blocked | 0 |
| Deliverables missing | 0 |
| Scope items covered | SOW-0303 (floor: L-003, L-005, L-006, L-007, L-008), SOW-0304 (foundation: L-001, L-002, L-009, L-010), plus REQ-06 aprons (L-004, L-005) |

## Blocker Check

**0 blockers identified.** All 12 dependency rows in Dependencies.csv are either anchor/traceability rows (DEP-04-03-001 through DEP-04-03-005) or design-execution prerequisites/interfaces (DEP-04-03-006 through DEP-04-03-012). None block proposal-stage estimating.

## Parametric Validation

| Validation | Expected Range | Actual | Status |
|---|---|---|---|
| Foundation + floor as % of PB-02 turnkey ($288,000) | 25-40% typical | 54.5% ($156,938) | HIGH -- explanation provided in Summary.md (screw piles + full concrete slab + sulphate mix drive higher allocation) |
| Cost per sf of building footprint | $20-$35/sf typical for foundation+floor | $26.16/sf ($156,938 / 6,000 sf) | WITHIN RANGE |
| Screw pile cost as % of total | 15-25% typical | 38.2% ($60,000 / $156,938) | HIGH -- 20 piles is conservative; validate pile count with PEMB manufacturer |

## What to Fix for a Cleaner Rerun

1. **Confirm pile count** with PEMB manufacturer or structural engineer. This is the single largest source of uncertainty ($60,000 / $156,938 = 38% of total).
2. **Confirm grade beam scope** (80 lm) with structural engineer. This is the second-largest source of uncertainty ($17,600 / $156,938 = 11% of total).
3. **Add direct rate table items** for subgrade preparation, granular base, and vapour barrier to eliminate derived rates and double-count risk.
4. **Confirm floor live load** (Datasheet [B-001]) to validate 150mm slab thickness selection.
5. **Clarify SC-03 scope** -- does "includes sub-base prep" in SC-03 notes include the specific radon rock layer, or only standard granular base? If it includes radon rock, remove L-007 ($8,355) to avoid double-counting.
6. **Confirm design life** (Datasheet [A-001]) -- if ancillary building has shorter design life, asphalt millings floor option could reduce cost by $30,000-$40,000.

## S8 -- Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | WARNINGS -- gaps are bounded and quantified |
| Basis-consistency checks pass | PASS -- all RATE_TABLE |
| Provenance completeness reported | 100% (3 derived rates documented) |
| Top gaps are actionable | YES -- pile count, grade beam qty, SC-03 scope clarification |
| Scope coverage is explicit | YES -- 1 deliverable, SOW-0303 + SOW-0304 covered |
| No writes outside _Estimates/ | CONFIRMED |
