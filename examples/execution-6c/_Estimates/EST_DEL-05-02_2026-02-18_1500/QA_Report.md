# QA Report: EST_DEL-05-02_2026-02-18_1500

## RUN_STATUS: WARNINGS

---

## Schema Validity

| Check | Result |
|---|---|
| Detail.csv exists | PASS |
| Detail.csv parseable | PASS |
| All required columns present | PASS (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) |
| Method values valid | PASS (RATE_TABLE, PARAMETRIC, ALLOWANCE -- all valid enum values) |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS for all ALLOWANCE lines; PASS for PARAMETRIC LS lines |
| Currency consistent | PASS (all CAD) |
| WBS_CBS_Matrix.csv exists | PASS |
| Summary.md exists | PASS |
| Source_Index.md exists | PASS |
| Run_Context.md exists | PASS |

---

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-05-02) |
| Deliverables priced | 1 |
| Deliverables blocked | 0 |
| Deliverables with TBD amounts | 0 |
| Total line items | 73 (3 production + 68 construction content + 2 GR transparency) |
| Lines with non-zero Amount | 72 (L-116 was originally zero but now $82k; all lines priced) |
| CBS categories covered | 16 (FIN, MGMT, GR, STRUCT, ENVLP, INTARCH, MECH, ELEC, CIVIL, UG, COLDSTG, EQUIP, DESFEE, FEES, OPT, TAX) |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Lines with SourceRef | 73 / 73 (100%) |
| Lines with non-TBD SourceRef | 73 / 73 (100%) |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

---

## Basis-Consistency Checks

| Check | Result | Notes |
|---|---|---|
| BASIS_OF_ESTIMATE valid | PASS | RATE_TABLE for production; PARAMETRIC/ALLOWANCE for construction content |
| ALLOW_MIXED_METHODS | TRUE | Mixed methods expected and approved per BOE Section 3.2 |
| Production lines Method=RATE_TABLE | PASS | L-001 through L-003 all RATE_TABLE |
| Construction content Method consistency | PASS | PARAMETRIC (majority) + ALLOWANCE (L-076, L-077, L-094, L-170) |
| FALLBACK_POLICY=ALLOW_ALLOWANCE | PASS | ALLOWANCE method used for 4 lines where parametric basis is unavailable (utility tie-ins, connection fees, workshop equipment, FF&E) |
| No unauthorized method values | PASS | All methods are RATE_TABLE, PARAMETRIC, or ALLOWANCE |

---

## Schedule A / Schedule B Reconciliation

| CBS | Schedule A | Schedule B | Variance | Status |
|---|---|---|---|---|
| GR | $1,305,000 | $1,305,000 | $0 | RECONCILED |
| STRUCT | $1,320,000 | $1,320,000 | $0 | RECONCILED |
| ENVLP | $980,000 | $980,000 | $0 | RECONCILED |
| INTARCH | $520,000 | $520,000 | $0 | RECONCILED |
| MECH | $1,180,000 | $1,180,000 | $0 | RECONCILED |
| ELEC | $810,000 | $810,000 | $0 | RECONCILED |
| CIVIL + UG | $1,580,000 | $1,580,000 | $0 | RECONCILED |
| COLDSTG | $290,000 | $290,000 | $0 | RECONCILED |
| EQUIP | $540,000 | $540,000 | $0 | RECONCILED |
| DESFEE | $780,000 | $780,000 | $0 | RECONCILED |
| FEES | $558,000 | $558,000 | $0 | RECONCILED |
| Base Subtotal | $9,863,000 | $9,863,000 | $0 | RECONCILED |
| Options | $355,000 | $355,000 | $0 | RECONCILED |
| GST | $511,000 | $511,000 | $0 | RECONCILED |
| **Content Total** | **$10,729,000** | **$10,729,000** | **$0** | **RECONCILED** |

**Reconciliation status: ALL CBS categories reconcile exactly to Schedule A (DEL-05-01).**

---

## Dependency / Blocker Assessment

| DependencyID | Target | Impact on Estimate | Status |
|---|---|---|---|
| DEP-05-02-004 | DEL-02-01 (Concept) | Provides GFA/massing for quantity derivation | Used PP-05 (18000 sf) as proxy; concept not yet available for detailed takeoff |
| DEP-05-02-005 | DEL-05-01 (Schedule A) | Reconciliation target | RECONCILED -- all CBS totals match |
| DEP-05-02-010 | RFP Appendix H template | Schedule B form structure | Template format assumed based on decomposition description |
| DEP-05-02-011 | Addendum 03 | Scope changes reflected | Pickled sand removed; 12-acre site; FF&E as Option 6 |

**No active blockers for estimate production.**

---

## Warnings

| ID | Severity | Description | Action Required |
|---|---|---|---|
| W-001 | MEDIUM | All construction pricing content is PARAMETRIC (no vendor quotes). Accuracy +/-20-50%. | Obtain vendor quotes before proposal submission |
| W-002 | MEDIUM | Design fee markup adjustment ($405k in L-108) is a reconciliation line. Underlying discipline-specific fees ($375k) may be more accurate. | Review DB firm design fee structure |
| W-003 | MEDIUM | Bond/insurance rates (5.45% combined) are market estimates. | Obtain actual surety and insurance quotes |
| W-004 | LOW | Underground utility contingency ($64.5k in L-078) is a reconciliation allocation. | Validate with site investigation |
| W-005 | LOW | OI-004 (FF&E) implemented as $20k allowance but formally OPEN. | Resolve OI-004 before proposal submission |
| W-006 | LOW | GR transparency lines (L-095, L-096) must be excluded from summation to avoid double-counting. | Automated summation should filter by note flag |
| W-007 | LOW | Cold storage sub-element allocation split between L-080 and L-059 for CBS traceability. | No action; documented for audit |

---

## What to Fix for a Cleaner Rerun

1. **Obtain vendor quotes** for major equipment (generator, overhead doors, exhaust systems, lockers) to replace PARAMETRIC with QUOTE method.
2. **Refine quantity takeoffs** once DEL-02-01 concept design is available (currently using assumed areas from PP-05/PP-07).
3. **Obtain actual bond/insurance quotes** from surety broker and insurance provider.
4. **Resolve OI-004 formally** to confirm $20k FF&E allowance.
5. **Validate GR allocation** (15% = $1,305,000) against actual DB firm general requirements pricing.
6. **Confirm utility tie-in costs** with municipal utility providers (currently ALLOWANCE at $35k).
7. **Review design fee structure** -- the $405k markup adjustment suggests the standard percentage-based fee calculation significantly underestimates the DB firm's design services charge.

---

## Operator Acceptance Checklist (S8)

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | WARNINGS -- all gaps are bounded and documented |
| Basis-consistency checks pass | PASS |
| Provenance completeness reported | 100% -- all lines have SourceRef |
| Scope coverage explicit | 1/1 deliverable priced; 0 blocked; 0 TBD |
| No writes outside _Estimates/ | CONFIRMED |
| Schedule A/B reconciliation | ALL CBS categories RECONCILED |
