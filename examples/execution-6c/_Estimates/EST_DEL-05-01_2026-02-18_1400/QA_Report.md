# QA Report: EST_DEL-05-01_2026-02-18_1400

## RUN_STATUS: WARNINGS

---

## S1 -- Write Quarantine

| Check | Result |
|---|---|
| All files written under _Estimates/ | PASS |
| No project truth files modified | PASS |
| No deliverable content files modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition files modified | PASS |
| No dependency registers modified | PASS |

---

## S2 -- Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | PASS |
| Folder path | EST_DEL-05-01_2026-02-18_1400 |

---

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE provided | PASS |
| Value | RATE_TABLE (primary; with PARAMETRIC and ALLOWANCE per ALLOW_MIXED_METHODS=TRUE) |
| Enum validation | PASS (RATE_TABLE is a valid enum value) |
| Mixed methods authorized | PASS (ALLOW_MIXED_METHODS=TRUE in brief) |

---

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

---

## S5 -- Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv is parseable | PASS |
| Required columns present (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid | PASS (RATE_TABLE: 3 lines; PARAMETRIC: 18 lines; ALLOWANCE: 1 line) |
| Allowance convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS (L-035 FF&E: Qty=1, Unit=LS, UnitRate=20000, Amount=20000) |
| All parametric lines use Qty=1, Unit=LS | PASS |
| Currency consistent (CAD) | PASS |
| Line count | 24 lines |

---

## S6 -- Provenance Discipline

| Check | Result |
|---|---|
| Lines with SourceRef | 24 / 24 (100%) |
| Lines with "location TBD" SourceRef | 0 |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

All 24 lines include specific file references and item IDs from PRICE_SOURCES.

---

## S7 -- Status Determination

**RUN_STATUS: WARNINGS**

Rationale:
- All deliverables in scope are priced (no TBD amounts).
- Provenance is 100% complete.
- However, material warnings remain that prevent OK status:
  - W-001: All construction content is PARAMETRIC (no vendor quotes; accuracy +/-20-50%)
  - W-002: Design fee calculation uses blended percentage (actual DB fee structure may differ)
  - W-003: Bond/insurance rates are market estimates (actual quotes needed)
  - W-005: OI-004 (FF&E) is formally OPEN even though recommended resolution is applied

---

## Schema Validation Detail

### Method Distribution

| Method | Line Count | Amount Total (CAD) | Percentage of Total |
|---|---|---|---|
| RATE_TABLE | 3 | $9,960 | 0.1% |
| PARAMETRIC | 20 | $10,709,000 | 99.7% |
| ALLOWANCE | 1 | $20,000 | 0.2% |
| **TOTAL** | **24** | **$10,738,960** | **100%** |

### Basis Consistency

| Check | Result |
|---|---|
| Primary BASIS_OF_ESTIMATE | RATE_TABLE |
| ALLOW_MIXED_METHODS | TRUE |
| Methods present | RATE_TABLE, PARAMETRIC, ALLOWANCE |
| Basis consistency | PASS (mixed methods authorized; production lines use RATE_TABLE; construction content uses PARAMETRIC/ALLOWANCE as expected for dual-nature deliverable) |
| FALLBACK_POLICY | ALLOW_ALLOWANCE |
| Fallback used | YES (L-035 FF&E uses ALLOWANCE method per OI-004) |

---

## Coverage Analysis

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables fully priced | 1 |
| Deliverables partially priced | 0 |
| Deliverables blocked | 0 |
| Deliverables with TBD amounts | 0 |
| Line items total | 24 |
| Production cost lines | 3 |
| Construction content lines | 21 |

### Schedule A Structure Completeness

| Schedule A Section | Covered | Lines |
|---|---|---|
| Base building (structure, envelope, MEP, interior) | YES | L-011 through L-015, L-018 |
| General requirements | YES | L-010 |
| Site/civil works | YES | L-016, L-017 |
| Specialty equipment | YES | L-019 |
| Design fees | YES | L-020 |
| Bonds and insurance | YES | L-021 |
| Permits and fees | YES | L-022 |
| Additional Option 1 (Wash Bay) | YES | L-030 |
| Additional Option 2 (Yard Lighting) | YES | L-031 |
| Additional Option 3 (Access Control) | YES | L-032 |
| Additional Option 4 (Security/Cameras) | YES | L-033 |
| Additional Option 5 (Signage) | YES | L-034 |
| Additional Option 6 (FF&E/Appliances) | YES | L-035 |
| GST (taxes separated) | YES | L-040, L-041 |
| Addenda acknowledgment | NOTED | Covered in L-010 notes and Assumptions_Log.md |

---

## Blocker Analysis (from Dependencies.csv)

| DependencyID | Type | Target | Impact on Estimate |
|---|---|---|---|
| DEP-05-01-E-001 | PREREQUISITE | DEL-05-02 (Schedule B) | Production dependency only -- Schedule B must be substantially complete before Schedule A form can be finalized. Does NOT block the ESTIMATE (pricing can be estimated independently). |
| DEP-05-01-E-002 | INTERFACE | DEL-01-03 (Bonding) | Bond cost data needed in Schedule A. Estimated parametrically using FP-01/FP-02 rates. |
| DEP-05-01-E-007 | PREREQUISITE | RFP Appendix H template | Template required for form completion. Does not block estimate. |
| DEP-05-01-E-008 | PREREQUISITE | Addendum 03 | Pricing impacts incorporated. |

**Blockers preventing meaningful estimating: 0**

---

## Warnings Register

| ID | Warning | Severity | Recommendation |
|---|---|---|---|
| W-001 | All construction content is PARAMETRIC -- no vendor quotes | MEDIUM | Obtain subtrade quotes for major scope packages (structural, mechanical, electrical) before proposal submission |
| W-002 | Design fee at 9% of base construction is a blended assumption | LOW | Confirm actual DB firm design fee structure |
| W-003 | Bond/insurance rates (5.45% combined) are market estimates | LOW | Obtain actual surety and insurance quotes |
| W-004 | Parametric cross-check shows 11% variance from PP-25 ($12M) | LOW | Variance is within acceptable range for LOW confidence parametric |
| W-005 | OI-004 (FF&E) is formally OPEN; $20k allowance applied per recommendation | MEDIUM | Resolve OI-004 formally before proposal submission |

---

## What to Fix for a Cleaner Rerun

1. **Obtain vendor quotes** for at least structural steel, mechanical systems, and electrical scope to move from PARAMETRIC to QUOTE method.
2. **Resolve OI-004 formally** to change FF&E line from ALLOWANCE to confirmed pricing.
3. **Confirm design fee structure** with actual DB firm rates to validate the 9% blended percentage.
4. **Obtain surety and insurance quotes** to refine bond/insurance line items.
5. **Complete Schedule B (DEL-05-02)** to provide a bottom-up validation of Schedule A summary totals.
6. If vendor quotes are obtained, rerun with `FALLBACK_POLICY=STRICT` and `ALLOW_MIXED_METHODS=FALSE` to produce a cleaner RATE_TABLE/QUOTE-only estimate.
