# QA Report: EST_DEL-05-03_2026-02-18_1430

## RUN_STATUS: OK

---

## S1 -- Write Quarantine

| Check | Result |
|---|---|
| All writes under ESTIMATES_ROOT? | PASS -- all files written to _Estimates/EST_DEL-05-03_2026-02-18_1430/ |
| No modifications to deliverable content, lifecycle files, decomposition, or dependency registers? | PASS |

---

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists? | PASS -- EST_DEL-05-03_2026-02-18_1430/ created |

---

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE present? | PASS |
| BASIS_OF_ESTIMATE value valid? | PASS -- RATE_TABLE is a valid enum value |
| Consistent with BOE per-deliverable plan? | PASS -- BOE Section 4 specifies RATE_TABLE for DEL-05-03 |

---

## S4 -- Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Detail.csv | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |

---

## S5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv parseable? | PASS |
| All required columns present? | PASS -- LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes |
| Method values valid? | PASS -- all RATE_TABLE |
| Allowance/parametric convention? | N/A -- no ALLOWANCE or PARAMETRIC lines |
| Amount calculation correct? | PASS -- L-001: 12 x 175 = 2100; L-002: 8 x 145 = 1160; Total: 3260 |
| Rounding applied? | PASS -- all amounts are whole dollars (DOLLAR rounding) |

---

## S6 -- Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows | 2 |
| Rows with SourceRef | 2 |
| Rows with "location TBD" | 0 |
| **Provenance completeness** | **100%** |
| Top missing-source offenders | None |

---

## S7 -- Status Reporting

**RUN_STATUS: OK**

Rationale:
- All line items priced with RATE_TABLE method from available pricing sources
- No TBD amounts
- No critical input gaps
- Provenance is 100% complete
- Basis consistency is maintained (all lines RATE_TABLE per ALLOW_MIXED_METHODS=FALSE)

---

## Basis Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| ALLOW_MIXED_METHODS | FALSE |
| Method values in Detail.csv | RATE_TABLE (L-001), RATE_TABLE (L-002) |
| All methods match basis? | PASS |
| Deviations? | None |

---

## Scope Coverage

| Metric | Count |
|---|---|
| Deliverables in scope | 1 |
| Deliverables priced | 1 |
| Deliverables blocked | 0 |
| Deliverables with TBD amounts | 0 |
| Deliverables excluded | 0 |

---

## Dependency-Derived Blocker Assessment

| DependencyID | Target | Type | EstimateImpactClass | Status |
|---|---|---|---|---|
| DEP-05-03-004 | DEL-05-01 (Schedule A) | INTERFACE | BLOCKING | Resolved for estimating -- upstream estimate available ($10,738,960) |
| DEP-05-03-005 | DEL-05-02 (Schedule B) | INTERFACE | BLOCKING | Resolved for estimating -- upstream estimate available ($10,735,020) |
| DEP-05-03-013 | RFP 2024_004 | CONSTRAINT | BLOCKING | Resolved -- RFP is a governing document; compliance requirements integrated into narrative scope |
| DEP-05-03-006 | DEL-02-01 (Concept) | PREREQUISITE | ADVISORY | Not blocking for production cost estimation |
| DEP-05-03-007 | DEL-02-02 (Design Brief) | PREREQUISITE | ADVISORY | Not blocking for production cost estimation |
| DEP-05-03-008 | DEL-04-01 (Construction Methodology) | PREREQUISITE | ADVISORY | Not blocking for production cost estimation |
| DEP-05-03-009 | DEL-08-01 (Schedule) | PREREQUISITE | ADVISORY | Not blocking for production cost estimation |
| DEP-05-03-010 | DEL-09-02 (Site Conditions) | PREREQUISITE | ADVISORY | Not blocking for production cost estimation |
| DEP-05-03-014 | Addendum 03 | CONSTRAINT | BLOCKING | Resolved -- integrated into decomposition |

**Unresolved blockers: 0**

---

## Warnings Summary

| ID | Warning | Severity | Actionable? |
|---|---|---|---|
| W-001 | OI-004 (FF&E) formally OPEN; assumed as $20k allowance in upstream estimates | LOW | Yes -- resolve OI-004 before narrative finalization |
| W-002 | Upstream construction pricing is PARAMETRIC (no vendor quotes) | LOW | Yes -- obtain quotes to improve accuracy |
| W-003 | Level-of-effort hours are PARAMETRIC estimates (+/-20-30%) | LOW | Yes -- track actual hours during production |
| W-004 | Value alternatives analysis may require additional discipline hours beyond PM allocation | LOW | Yes -- monitor scope during production |

---

## Operator Acceptance Checklist (S8)

| Check | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps? | PASS -- OK |
| Basis-consistency checks pass? | PASS |
| Provenance completeness reported? | PASS -- 100% |
| Scope coverage explicit? | PASS -- 1 included, 0 excluded, 0 blocked |
| No writes outside _Estimates/? | PASS |
| **Snapshot publishable?** | **YES** |
