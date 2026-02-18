# QA Report

## Snapshot Identification

| Field | Value |
|-------|-------|
| **Snapshot ID** | EST_DEL-01-02_2026-02-04_1322 |
| **Deliverable** | DEL-01-02 FormalSubmissionPackage |
| **RUN_STATUS** | WARNINGS |

---

## QA Checks

### Currency Consistency

| Check | Result |
|-------|--------|
| Currency specified | CAD |
| All line items use same currency | PASS |
| Mixed currencies | None |
| Conversion assumptions required | No |

**Status:** PASS

---

### Qty/Unit/UnitRate Completeness

| Check | Result |
|-------|--------|
| Total line items | 16 |
| Lines with Qty populated | 16 |
| Lines with Unit populated | 16 |
| Lines with UnitRate populated | 16 |
| Lines with Amount populated | 16 |
| Missing any required field | None |

**Status:** PASS

---

### Arithmetic Reconciliation

| Check | Result |
|-------|--------|
| Sum of Detail.csv line items | $12,300 |
| Summary.md total | $12,300 |
| Variance | $0 |
| Within rounding tolerance | Yes |

**Status:** PASS

---

### Coverage Check

| Check | Result |
|-------|--------|
| Deliverables in scope | 1 (DEL-01-02) |
| Deliverables with cost lines | 1 |
| Deliverables with no cost lines | 0 |
| Coverage | 100% |

**Status:** PASS

---

### Double Count Heuristics

| Check | Result |
|-------|--------|
| Duplicate descriptions | None identified |
| Overlapping scope areas | None identified |
| Same WBS/CBS priced twice | No |

**Status:** PASS

---

### Unknowns List (Top Assumptions/Allowances by Value)

| Rank | ID | Description | Amount | Impact |
|------|-----|-------------|--------|--------|
| 1 | L-008 (A-010) | QA Review Team | $1,600 | Largest single line item |
| 2 | L-016 (D-006) | Contingency | $1,600 | Uncertainty reserve |
| 3 | L-002 (A-004) | Content File Collection | $1,200 | Dependent on upstream deliverable count |
| 4 | L-015 (A-017) | Revision Contingency | $1,000 | May not be needed |
| 5 | L-004 (A-006) | Graphics Optimization | $1,000 | File size dependent |
| 6 | L-005 (A-007) | PDF Assembly | $1,000 | Tool/template dependent |

**Note:** All line items are allowance-based; rankings reflect largest cost assumptions.

---

## Completeness Metrics

| Metric | Value |
|--------|-------|
| % of lines priced by QUOTE | 0% (0/16) |
| % of lines priced by RATE_TABLE | 0% (0/16) |
| % of lines priced by ALLOWANCE | 100% (16/16) |
| % of deliverables with explicit quantities extracted | 0% |
| Total labor hours estimated | 48 hours |
| Average implied hourly rate | ~$182/hr (blended) |

---

## Mapping Ambiguities

| Item | Ambiguity | Resolution | Decision ID |
|------|-----------|------------|-------------|
| CBS Assignment | Proposal management could be mapped to E (Engineering) or PM | Mapped to PM as primary; proposal management is EPCM-type overhead | D-002 |

---

## Known Issues

### ISSUE-001: No Rate Tables Available

| Field | Value |
|-------|-------|
| **Issue** | `_RateTables/` directory is empty; no project-specific labor rates available |
| **Impact** | All pricing is allowance-based with LOW confidence |
| **Severity** | Medium |
| **Resolution** | Provide labor rate tables (Proposal Manager, Graphics Coordinator, Admin) for future estimates |

---

### ISSUE-002: TBD Items in Source Documents

| Field | Value |
|-------|-------|
| **Issue** | Multiple TBD items in source documents: submission email address, RFP Section 6-9 headings, execution requirements by entity type |
| **Impact** | Uncertainty in effort estimates for Steps 3, 6; scope not fully defined |
| **Severity** | Low (for cost estimate); High (for deliverable completion) |
| **Resolution** | Resolve TBD items per Specification.md TBD Resolution Plan |

---

### ISSUE-003: No Historical Baseline

| Field | Value |
|-------|-------|
| **Issue** | No historical data for similar proposal management deliverables to calibrate estimates |
| **Impact** | Labor hour estimates are judgment-based; actual effort may vary significantly |
| **Severity** | Medium |
| **Resolution** | Track actual hours for DEL-01-02; use as baseline for future estimates |

---

### ISSUE-004: Upstream Dependency Uncertainty

| Field | Value |
|-------|-------|
| **Issue** | Estimate assumes all 20+ upstream deliverables (DEL-02 through DEL-09) are available on time |
| **Impact** | Delays could compress assembly timeline and increase overtime/rework |
| **Severity** | Medium |
| **Resolution** | Monitor upstream deliverable status; adjust timeline or contingency if delays occur |

---

## Run Status Determination

| Criterion | Status |
|-----------|--------|
| Critical failures (missing required fields, arithmetic errors) | None |
| Material assumptions/ambiguities | Yes (100% allowance-based, no rate tables) |
| Known issues requiring attention | 4 issues documented |
| Estimate usable for budgeting | Yes, with LOW confidence |

**RUN_STATUS: WARNINGS**

- Estimate is complete and arithmetically correct
- All required artifacts produced
- However, estimate has LOW confidence due to 100% allowance-based pricing
- Multiple known issues require attention for improved accuracy

---

## Recommendations

1. **Provide rate tables** — Add labor rate tables to `_RateTables/` for future estimates
2. **Resolve TBD items** — Complete TBD Resolution Plan before next estimate iteration
3. **Track actuals** — Compare actual effort to estimate after proposal submission
4. **Review assumptions** — Validate labor hour assumptions with experienced proposal managers
5. **Update contingency** — Consider adjusting contingency if rate tables and historical data become available
