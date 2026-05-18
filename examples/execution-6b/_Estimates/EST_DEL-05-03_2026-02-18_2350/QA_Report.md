# QA Report -- EST_DEL-05-03_2026-02-18_2350

## RUN_STATUS: OK

---

## 1. Schema Validity (Detail.csv)

| Check | Result |
|---|---|
| Detail.csv exists and is parseable | PASS |
| All required columns present (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (RATE_TABLE) | PASS |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount) | N/A -- no ALLOWANCE or PARAMETRIC method rows |
| Amount = Qty x UnitRate for all rows | PASS (8 x 160 = 1280) |
| Currency consistent (CAD) | PASS |

## 2. Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-05-03) |
| Deliverables with at least one priced line | 1 (100%) |
| Deliverables with all TBD amounts | 0 |
| Deliverables blocked | 0 |

## 3. Provenance Completeness

| Metric | Value |
|---|---|
| Total priced rows | 1 |
| Rows with non-TBD SourceRef | 1 (100%) |
| Rows with TBD SourceRef | 0 |
| Top missing-source offenders | None |

## 4. Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE declared | RATE_TABLE |
| Method values in Detail.csv | RATE_TABLE (1 row) |
| Mixed methods detected | NO |
| ALLOW_MIXED_METHODS setting | FALSE |
| Consistency | PASS -- all methods match declared basis |

## 5. Blocker Assessment (from Dependencies.csv)

| Dependency | Type | Status | Impact on Estimate |
|---|---|---|---|
| DEP-05-03-003: DEL-02-04 (Mechanical Concept Narrative) | PREREQUISITE | PENDING | No pricing impact. Upstream deliverable defines baseline mechanical system selections that DEL-05-03 elaborates. Does not change hours or rate. |
| DEP-05-03-004: DEL-04-02 (Mechanical Energy & Solar Readiness) | PREREQUISITE | PENDING | No pricing impact. Upstream deliverable provides equipment selections and efficiency ratings. Does not change hours or rate. |
| DEP-05-03-006: DEL-05-01 (Architectural Durability) | INTERFACE | TBD | No pricing impact. Coordination interface for building finish and access provisions. |
| DEP-05-03-007: DEL-05-02 (Structural Durability) | INTERFACE | TBD | No pricing impact. Coordination interface for structural support and sump pit design. |

**Blocker count: 0 (no dependencies block pricing; 2 prerequisites are PENDING but do not affect the estimate amount)**

## 6. Rounding Verification

| Check | Result |
|---|---|
| Rounding policy | DOLLAR |
| All amounts are whole dollars | PASS (1280 is already a whole dollar amount) |

## 7. Write Quarantine

| Check | Result |
|---|---|
| All files written under _Estimates/ | PASS |
| No files modified outside _Estimates/ | PASS |

## 8. What to Fix for a Cleaner Rerun

- Nothing required. This run is clean with full provenance, consistent basis, and complete coverage.
- If upstream deliverables (DEL-02-04, DEL-04-02) are later found to require additional mechanical engineering coordination hours, the Level_of_Effort.csv should be updated and this estimate rerun.
