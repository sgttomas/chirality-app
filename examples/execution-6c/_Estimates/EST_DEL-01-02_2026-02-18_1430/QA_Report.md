# QA Report — EST_DEL-01-02_2026-02-18_1430

**RunID:** EST_DEL-01-02_2026-02-18_1430
**AsOf:** 2026-02-18
**RUN_STATUS: OK**

---

## 1. Schema Validity (Detail.csv)

| Check | Result | Notes |
|-------|--------|-------|
| All required columns present | PASS | LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes |
| Method values valid | PASS | All rows: RATE_TABLE (valid enum) |
| Allowance/parametric convention | N/A | No ALLOWANCE or PARAMETRIC method rows |
| Amount = Qty x UnitRate | PASS | L-01: 14 x 105 = 1470; L-02: 4 x 175 = 700 |
| Currency consistent | PASS | All rows: CAD |
| Rounding applied | PASS | All amounts are whole dollars (DOLLAR rounding) |

---

## 2. Coverage

| Metric | Value |
|--------|-------|
| Deliverables in scope | 1 (DEL-01-02) |
| Deliverables covered (with priced lines) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items produced | 2 |
| Total hours | 18 |
| Total amount | $2,170 CAD |

---

## 3. Provenance Completeness

| Metric | Value |
|--------|-------|
| Total priced rows | 2 |
| Rows with non-TBD SourceRef | 2 |
| **Provenance completeness** | **100%** |
| Top missing-source offenders | None |

---

## 4. Basis-Consistency Checks

| Check | Result | Notes |
|-------|--------|-------|
| BASIS_OF_ESTIMATE declared | RATE_TABLE | Valid enum |
| All Detail.csv Method values match BASIS_OF_ESTIMATE | PASS | 2/2 rows = RATE_TABLE |
| ALLOW_MIXED_METHODS = FALSE enforced | PASS | No mixed methods |
| FALLBACK_POLICY = STRICT enforced | PASS | No fallback pricing used; all lines have basis evidence |

---

## 5. Blocker Report (from Dependency Evidence)

| Metric | Value |
|--------|-------|
| Total upstream prerequisites | 20 deliverables |
| Prerequisites at PENDING | 20 |
| Prerequisites satisfied | 0 |
| **Estimation blocked?** | **NO** -- production hours are estimable independently of content readiness |

**Note:** While all 20 upstream deliverables are PENDING, this does not block the *estimate* of DEL-01-02's production cost. The hours required to assemble, QA, and submit the final PDF are independent of whether the upstream content exists yet. The dependency matters for *execution* (can't assemble what doesn't exist), not for *estimating* (can estimate the assembly effort).

### Upstream Prerequisite Summary

| TargetDeliverableID | TargetName | SatisfactionStatus | RequiredMaturity |
|---------------------|------------|-------------------|------------------|
| DEL-01-01 | Compliance Matrix & Checklist | PENDING | Final |
| DEL-01-03 | Bonding & Insurance Evidence | PENDING | Final (executed) |
| DEL-02-01 | Concept Design Package | PENDING | Final |
| DEL-02-02 | Design Brief Narrative | PENDING | Final |
| DEL-02-03 | Sustainability & Energy Narrative | PENDING | Final |
| DEL-03-01 | Design Methodology Narrative | PENDING | Final |
| DEL-03-02 | Detailed Design & Construction Docs Plan | PENDING | Final |
| DEL-04-01 | Construction Methodology Narrative | PENDING | Final |
| DEL-04-02 | Budget Control & Change Management Plan | PENDING | Final |
| DEL-04-03 | Communications & Reporting Plan | PENDING | Final |
| DEL-05-01 | Schedule A -- Pricing Summary | PENDING | Final (executed) |
| DEL-05-02 | Schedule B -- Cost Breakdown | PENDING | Final |
| DEL-05-03 | Pricing Narrative & Assumptions | PENDING | Final |
| DEL-06-01 | Commissioning/Training/Closeout/Warranty | PENDING | Final |
| DEL-07-01 | DB Firm Experience Profile | PENDING | Final |
| DEL-07-02 | Key Team Members & Resumes | PENDING | Final |
| DEL-07-03 | Appendix I -- Subtrade & Consultant List | PENDING | Final |
| DEL-08-01 | Detailed Project Schedule | PENDING | Final |
| DEL-09-01 | Risk Register & Mitigation Plan | PENDING | Final |
| DEL-09-02 | Site Conditions & Due Diligence Summary | PENDING | Final |

---

## 6. Warnings

| ID | Severity | Description |
|----|----------|-------------|
| W-01 | INFO | TERMINAL_DELIVERABLE: DEL-01-02 is Tier 5, the last deliverable in the production sequence. All 20 upstream prerequisites are PENDING. This is expected at this stage. |
| W-02 | INFO | Rate and hour confidence is MEDIUM (+/-20-30%). Actual firm rates and actual assembly effort may vary. |

---

## 7. What to Fix for a Cleaner Rerun

- No critical issues. This is a clean run with 100% provenance completeness and consistent basis.
- If actual firm rates become available (replacing parametric market rates), rerun with updated Professional_Staff_Rates.csv for higher confidence.
- If actual assembly hours are known from a prior proposal effort, update Level_of_Effort.csv for DEL-01-02 rows and rerun.

---

## 8. Operator Acceptance Checklist

| Check | Status |
|-------|--------|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (OK) |
| Basis-consistency checks pass | PASS |
| Provenance completeness reported | PASS (100%) |
| Scope coverage explicit | PASS (1/1 deliverable covered) |
| No writes outside _Estimates/ | PASS |
