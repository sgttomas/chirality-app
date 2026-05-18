# QA Report: EST_DEL-01-03_2026-02-18_1500

## RUN_STATUS: WARNINGS

---

## Schema Validity

| Check | Result | Notes |
|---|---|---|
| Detail.csv parseable | PASS | 9 data rows + header |
| All required columns present | PASS | LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes |
| Method values valid | PASS | RATE_TABLE (3 lines), ALLOWANCE (6 lines) |
| Allowance convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS | Lines L-010, L-011, L-020, L-021, L-022, L-030 all follow convention |
| Currency consistent | PASS | All lines = CAD |
| WBS_PackageID consistent | PASS | All lines = PKG-01 |
| WBS_DeliverableID consistent | PASS | All lines = DEL-01-03 |

---

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-01-03) |
| Deliverables priced | 1 |
| Deliverables blocked | 0 |
| Deliverables with TBD amounts | 0 |
| Lines priced | 9 |
| Lines with TBD amounts | 0 |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Total priced lines | 9 |
| Lines with non-TBD SourceRef | 9 |
| Lines with TBD SourceRef | 0 |
| **Provenance completeness** | **100%** |

---

## Basis-Consistency Checks

| Check | Result | Notes |
|---|---|---|
| BOE declared BASIS_OF_ESTIMATE | RATE_TABLE (with ALLOW_ALLOWANCE fallback) | Per BOE Section 4 PKG-01 table: DEL-01-03 |
| ALLOW_MIXED_METHODS | TRUE | Authorized in brief |
| Production lines method | RATE_TABLE (3 lines) | Consistent with BOE primary basis |
| Premium/fee lines method | ALLOWANCE (6 lines) | Authorized by FALLBACK_POLICY=ALLOW_ALLOWANCE |
| Method mix justified | PASS | Bond/insurance premiums are inherently percentage-based allowances; no rate table alternative exists for these items |

---

## Dependency-Informed Checks

| DependencyID | Type | Target | Status | Estimating Impact |
|---|---|---|---|---|
| DEP-01-03-005 | CONSTRAINT | RFP Section 5.3.1 | PENDING | Bond types/amounts assumed standard. If Section 5.3.1 specifies different requirements, estimate must be revised. |
| DEP-01-03-006 | PREREQUISITE | DEL-05-01 (Schedule A) | SATISFIED | Contract value basis ($9,863,000) obtained from EST_DEL-05-01_2026-02-18_1400 |
| DEP-01-03-007 | INTERFACE | DEL-05-02 (Schedule B) | PENDING | Bond figure reconciliation with Schedule B not yet confirmed |

---

## Arithmetic Verification

| Check | Expected | Actual | Result |
|---|---|---|---|
| Production subtotal | 700 + 1200 + 160 = 2060 | $2,060 | PASS |
| Bond subtotal | 147945 + 98630 = 246575 | $246,575 | PASS |
| Insurance subtotal | 197260 + 19726 + 73973 = 290959 | $290,959 | PASS |
| L-010 calculation | 9863000 x 0.015 = 147945 | $147,945 | PASS |
| L-011 calculation | 9863000 x 0.010 = 98630 | $98,630 | PASS |
| L-020 calculation | 9863000 x 0.020 = 197260 | $197,260 | PASS |
| L-021 calculation | 9863000 x 0.002 = 19726 | $19,726 | PASS |
| L-022 calculation | 9863000 x 0.0075 = 73972.50 -> 73973 | $73,973 | PASS (rounded up to nearest dollar) |
| Grand total | 2060 + 246575 + 290959 + 3500 = 543094 | $543,094 | PASS |

---

## Warnings Summary

| ID | Severity | Description | Action Required |
|---|---|---|---|
| W-001 | MEDIUM | All bond/insurance premiums are ALLOWANCE at MARKET rates; no actual quotes | Obtain surety and insurance quotes before submission |
| W-002 | HIGH | Contract value basis ($9,863,000) is PARAMETRIC; premiums will change with actual construction pricing | Recalculate premiums when construction pricing is finalized |
| W-003 | MEDIUM | RFP Section 5.3.1 not yet extracted; bond requirements assumed standard | Extract and verify bond types/amounts from RFP |
| W-004 | MEDIUM | CCIP rate (2.0%) has LOW confidence | Obtain actual CCIP quote for project |
| W-005 | LOW | DEL-05-01/05-02 reconciliation not yet confirmed for bond line items | Verify consistency when Schedule B estimate is available |

---

## What to Fix for a Cleaner Rerun

1. **Extract RFP Section 5.3.1** to confirm bond types, amounts, and format requirements (resolves W-003, DEP-01-03-005).
2. **Obtain actual surety quotes** for performance and L&M bonds (resolves W-001).
3. **Obtain actual insurance quotes** for CCIP, builder's risk, and CGL (resolves W-001, W-004).
4. **Finalize construction pricing** in DEL-05-01 to update the contract value basis (resolves W-002).
5. **Verify bond line reconciliation** with DEL-05-02 Schedule B estimate (resolves W-005).

---

## Operator Acceptance Checklist (S8)

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | WARNINGS -- gaps are clearly identified and bounded |
| Basis-consistency checks pass | PASS -- mixed methods authorized and justified |
| Provenance completeness reported | 100% -- all lines have SourceRef |
| Scope coverage explicit | 1/1 deliverable priced; 0 blocked; 0 TBD |
| No writes outside _Estimates/ | CONFIRMED |
