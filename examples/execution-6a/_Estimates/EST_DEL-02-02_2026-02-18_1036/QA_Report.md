# QA Report: EST_DEL-02-02_2026-02-18_1036

## RUN_STATUS: WARNINGS

Some totals exist but material assumptions remain regarding support room sizing and compressed air piping allowance. No critical input gaps prevent meaningful pricing.

---

## S1 -- Write Quarantine Respected

| Check | Result |
|---|---|
| All files written under ESTIMATES_ROOT | PASS |
| No deliverable content modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition outputs modified | PASS |
| No dependency registers modified | PASS |

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | PASS -- EST_DEL-02-02_2026-02-18_1036/ |

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE provided | PASS -- RATE_TABLE |
| Value is valid enum | PASS |

## S4 -- Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT |

## S5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv parseable | PASS |
| All 14 required columns present | PASS -- LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes |
| Method values valid | PASS -- 37x RATE_TABLE, 1x ALLOWANCE (both valid enums) |
| Allowance convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS -- L-004 (LS, Qty=1, UnitRate=Amount) and L-005 (LS, Qty=1, UnitRate=Amount) follow convention |
| Amount = Qty x UnitRate (for non-LS lines) | PASS -- spot-checked L-001 (780x35=27300), L-003 (40x2200=88000), L-006 (4x4500=18000) |
| Total line count | 38 lines |

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total priced lines | 38 |
| Lines with non-TBD SourceRef | 38 |
| Lines with TBD SourceRef | 0 |
| **Provenance completeness** | **100%** |

All 38 lines include a SourceRef pointing to a specific price source file and ItemID (or to a Decision_Log entry for the allowance line).

### Top Missing-Source Offenders

None -- all lines have provenance.

## S7 -- Basis-Consistency Checks

| Check | Result |
|---|---|
| Primary basis | RATE_TABLE |
| RATE_TABLE lines | 37 (97.4%) |
| ALLOWANCE lines | 1 (2.6%) -- L-005 compressed air piping |
| ALLOW_MIXED_METHODS | TRUE -- mixed methods permitted |
| FALLBACK_POLICY | ALLOW_ALLOWANCE -- allowance fallback permitted |
| Basis consistency | PASS -- 1 allowance line is explicitly authorized by FALLBACK_POLICY |

## S8 -- Coverage Assessment

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-02-02) |
| Deliverables with line items | 1 |
| Deliverables blocked | 0 |
| Deliverables missing | 0 |
| Scope items covered | SOW-0202, SOW-0203, SOW-0205, SOW-0206 |

### Scope Coverage by SOW Item

| SOW Item | Covered | Lines | Notes |
|---|---|---|---|
| SOW-0202 (4 apparatus bays) | YES | L-001, L-002, L-006 | Bay floor finish, ceiling paint, sumps. Overhead doors and structural shell excluded per ownership rules. |
| SOW-0203 (bay services -- electrical, compressed air, exhaust) | PARTIAL | L-004, L-005 | Compressed air equipment and piping covered. Electrical feed to DEL-02-06. Exhaust systems to DEL-02-05. |
| SOW-0205 (decontamination area + support spaces) | YES | L-007 through L-012, L-022 through L-036 | Decon area fit-up and all support room fit-up covered. |
| SOW-0206 (40 bunker gear lockers) | YES | L-003, L-013 through L-016, L-038 | Lockers and locker room fit-up covered. |

## Blocker Assessment (from dependency evidence)

| DependencyID | Type | Status | Impact on Estimate |
|---|---|---|---|
| DEP-0202-E01 | PREREQUISITE (DEL-02-01) | TBD | LOW -- floor plan zone allocation affects room sizing but midpoint assumptions used |
| DEP-0202-E02 | INTERFACE (DEL-02-04) | TBD | NONE -- overhead doors excluded from DEL-02-02 estimate |
| DEP-0202-E03 | INTERFACE (DEL-02-05) | TBD | NONE -- exhaust systems and plumbing excluded from DEL-02-02 estimate |
| DEP-0202-E04 | INTERFACE (DEL-02-06) | TBD | NONE -- electrical excluded from DEL-02-02 estimate |
| DEP-0202-E05 | INTERFACE (DEL-02-07) | TBD | NONE -- generator excluded from DEL-02-02 estimate |
| DEP-0202-E06 | INTERFACE (DEL-03-01) | TBD | LOW -- bay orientation does not materially change fit-up cost |
| DEP-0202-E09 | CONSTRAINT (Alberta Building Code) | PENDING | LOW -- may affect code compliance but does not directly affect pricing |

**Blockers preventing meaningful estimate: 0**

## Confidence Distribution

| Confidence | Line Count | Amount (CAD) | % of Total |
|---|---|---|---|
| LOW | 2 | $75,000 | 26.9% |
| MED | 36 | $204,279 | 73.1% |
| HIGH | 0 | $0 | 0.0% |

## What to Fix for a Cleaner Rerun

1. **Confirm support room areas** with architectural program output from DEL-02-01 to replace midpoint assumptions (ASM-002 through ASM-008).
2. **Obtain detailed compressed air piping routing** to replace the $20,000 allowance (L-005) with a measured quantity and rate.
3. **Finalize breathing air compressor system selection** to narrow the $45k-$65k range and improve confidence from LOW to MED.
4. **Verify bunker gear locker specification** (ventilated vs. non-ventilated, size, material) to confirm the $2,200 unit rate.
5. **Resolve DEP-0202-E01** (DEL-02-01 architectural program) for confirmed room areas and partition layouts.
