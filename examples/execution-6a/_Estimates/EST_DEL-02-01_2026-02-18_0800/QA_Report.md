# QA Report — EST_DEL-02-01_2026-02-18_0800

## RUN_STATUS: WARNINGS

Some totals exist but material TBDs and assumptions remain. The estimate is partially priced ($47,200 CAD across 3 line items) with 7 line items at TBD due to insufficient rate table evidence under STRICT fallback policy.

---

## S1 — Write Quarantine

| Check | Result |
|---|---|
| All writes under ESTIMATES_ROOT? | PASS |
| Any writes outside _Estimates/? | NO |

**Result: PASS**

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists? | PASS |
| Folder name | EST_DEL-02-01_2026-02-18_0800 |

**Result: PASS**

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| Value provided? | YES |
| Value | RATE_TABLE |
| Valid enum? | YES (RATE_TABLE is in {QUOTE, RATE_TABLE, HISTORICAL, PARAMETRIC, ALLOWANCE}) |

**Result: PASS**

## S4 — Required Artifacts Exist

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

**Result: PASS**

## S5 — Detail Schema Integrity

| Check | Result |
|---|---|
| Detail.csv parseable? | YES |
| All required columns present? | YES (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid? | YES — all values are RATE_TABLE |
| Allowance/parametric convention? | N/A — no ALLOWANCE or PARAMETRIC method rows |

**Result: PASS**

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows (Amount is numeric) | 3 |
| Priced rows with non-TBD SourceRef | 3 (100%) |
| Total TBD rows (Amount = TBD) | 7 |
| TBD rows with SourceRef = "location TBD" | 6 |
| TBD rows with valid SourceRef (explaining why TBD) | 1 (L-010: DF-01 identified but computation blocked) |
| **Overall provenance completeness (priced rows)** | **100%** |

### Top Missing-Source Items

| LineID | Description | Issue |
|---|---|---|
| L-004 | Interior partition walls | No rate in any provided source file |
| L-005 | Sealed concrete floor finish | Slab rates exist (SC-03/SC-04) but cover full slab (DEL-02-04); no finish-only rate |
| L-006 | Ceiling system | No rate in any provided source file |
| L-007 | Accessibility features | No rate in any provided source file |
| L-008 | Code-required signage | No rate in any provided source file |
| L-009 | Interior paint | Painter labour rate (T-12) exists but no combined material+labour rate |

**Result: PASS (provenance discipline met; TBD items are explicitly flagged)**

## S7 — Status Reporting

| Check | Result |
|---|---|
| RUN_STATUS declared? | YES |
| Value | WARNINGS |
| Justification | 3 of 10 line items priced ($47,200 CAD); 7 items TBD; construction subtotal incomplete; design fee cannot be computed |

**Result: PASS**

## Coverage Analysis

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-02-01) |
| Deliverables with at least 1 priced line | 1 |
| Deliverables fully priced | 0 |
| Total line items | 10 |
| Priced line items | 3 (30%) |
| TBD line items | 7 (70%) |

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| ALLOW_MIXED_METHODS | FALSE |
| All Method values = RATE_TABLE? | YES |
| Fallback methods used? | NO (STRICT policy; TBD used instead) |

**Result: PASS**

## Dependency / Blocker Analysis

| Metric | Value |
|---|---|
| Dependencies loaded | 23 (from Dependencies.csv) |
| Upstream execution dependencies | 6 |
| Downstream interfaces | 7 |
| Pricing-relevant blockers | 0 |
| Design-execution blockers (informational) | 2 (Functional Program location TBD; Alberta Building Code not accessible) |

Note: Dependency blockers (DEP-02-01-011, DEP-02-01-014) affect design execution, not pricing methodology. They indirectly affect quantity accuracy (shared-space areas are estimated, not confirmed).

## What to Fix for a Cleaner Rerun

1. **Add interior construction rate tables** to PRICE_SOURCES:
   - Interior partitions (metal stud + gypsum board): $/sf of wall face
   - Suspended acoustical ceiling tile: $/sf
   - Concrete floor sealer/hardener: $/sf (finish-only)
   - Interior paint: $/sf (material + labour combined)
   - Accessibility provisions: $/sf or lump sum
   - Code-required signage: lump sum or per-sign rate

2. **Obtain Functional Program (Appendix B)** to confirm shared-space areas and room counts. This will improve quantity accuracy for partitions, doors, and finishes.

3. **Consider FALLBACK_POLICY=ALLOW_ALLOWANCE** if rate table entries cannot be sourced. This would allow TBD items to be priced as allowances from an allowance table.

4. **Alternatively, use BASIS_OF_ESTIMATE=PARAMETRIC** with a $/sf parametric model for the entire architectural interior scope, which may be more appropriate for this deliverable given the early design stage.

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps? | PASS | WARNINGS; gaps are explicitly identified and bounded (7 TBD line items with known scope) |
| Basis-consistency checks pass? | PASS | All methods = RATE_TABLE; no mixed methods |
| Provenance completeness reported? | PASS | 100% of priced rows have SourceRef |
| Scope coverage explicit? | PASS | 1 deliverable in scope; 10 line items; 3 priced / 7 TBD |
| No writes outside _Estimates/? | PASS | Verified |

**Snapshot is publishable with the understanding that it represents a partial estimate. The $47,200 total covers doors/hardware only and is not a complete DEL-02-01 estimate.**
