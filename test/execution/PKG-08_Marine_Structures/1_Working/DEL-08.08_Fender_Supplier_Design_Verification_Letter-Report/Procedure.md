# Procedure: DEL-08.08 Fender Supplier Design Verification Letter/Report

## Purpose

Define repeatable workflow to obtain and process **Fender Supplier Design Verification Letter/Report** for design verification and approvals.

**Deliverable intent:** Documents analysis and results for fender supplier design verification letter/report required for design verification and approvals. *(Source: Decomposition line 288)*

---

## Prerequisites

**Dependency mode:** NOT_TRACKED

**Required Inputs (TBD):**

| Input | Source | Status |
|---|---|---|
| Design berthing energy | DEL-08.06 | **TBD** |
| Fender model selected | Design/procurement | **TBD** |
| Fender performance data | DEL-08.07 | **TBD** |
| Operating conditions | Design basis | **TBD** |
| Reaction force limits | DEL-08.03 | **TBD** |
| ER verification requirements | ER | **TBD** |
| P.Eng. requirement | ER/jurisdiction | **TBD** |

---

## Procedure Steps

### Step 1: Prepare Verification Request
1. Extract ER clauses for supplier verification
2. Confirm P.Eng. requirement
3. Compile design inputs (energy, conditions, limits)
4. Prepare request letter to supplier

**Outputs:** ER register, certification requirement, design input package, request letter

---

### Step 2: Submit Request
1. Transmit design inputs to supplier
2. Request verification letter/report per ER
3. Request stamped calculations (if required)
4. Confirm delivery date/format

**Outputs:** Transmittal, request records

---

### Step 3: Receive and Review
1. Receive verification letter/report
2. Check completeness
3. Verify design inputs match project
4. Confirm P.Eng. present (if required)
5. Check calculations (if provided)

**Outputs:** Supplier deliverable, completeness checklist

---

### Step 4: Address Deficiencies (if any)
1. Document deficiencies
2. Request supplier response/revision
3. Receive and verify updated docs

**Outputs:** Deficiency list, updated deliverable

---

### Step 5: QA/QC Review
1. Submit for D&B Contractor technical review
2. Address comments
3. Obtain sign-off

**Outputs:** Review record, disposition log

---

### Step 6: Issue and Control
1. Finalize per document control
2. Issue with transmittal
3. Update `_STATUS.md`
4. Archive

**Outputs:** Final package, transmittal

---

## Requirement Coverage Matrix

| Req ID | Step(s) | Evidence |
|---|---|---|
| R-001 | 2, 3 | Letter/report + calculations |
| R-002 | 3, 4 | Complete verification statement |
| R-003 | 1, 2, 3 | Design inputs documented/verified |
| R-004 | 1, 2, 3 | P.Eng. certification confirmed |
| R-005 | 1, 5 | ER compliance, QA review |
| R-006 | 6 | Controlled issue |

---

## Verification Checkpoints

| Checkpoint | Hold Point |
|---|---|
| After Step 1: Request complete | No |
| After Step 3: Supplier response compliant | No |
| After Step 4: Deficiencies resolved | No |
| After Step 5: QA review complete | **Yes** |
| After Step 6: Controlled issue | No |

---

## Sources

- Decomposition line 288
- `Specification.md` R-001 through R-006
