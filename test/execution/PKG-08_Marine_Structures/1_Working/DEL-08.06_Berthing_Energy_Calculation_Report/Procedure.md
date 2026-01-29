# Procedure: DEL-08.06 Berthing Energy Calculation Report

## Purpose

Define repeatable workflow for producing the **Berthing Energy Calculation Report** for design verification and approvals.

**Deliverable intent:** Documents analysis and results for berthing energy calculation report required for design verification and approvals. *(Source: Decomposition line 286)*

---

## Prerequisites

**Dependency mode:** NOT_TRACKED

**Required Inputs (TBD):**
- Design vessel particulars (from ER/project basis)
- Berthing scenarios and approach conditions (from ER/operations basis)
- Site environmental data (from ER/DEL-08.10)
- Applicable ER clauses and standards

---

## Procedure Steps

### Step 1: Establish Design Basis
1. Extract ER clauses for berthing energy
2. Identify design vessel(s) from ER
3. Define berthing scenarios (normal/abnormal)
4. Confirm standards and methodology (PIANC, BS 6349-4, etc.)

**Outputs:** ER clause register, vessel particulars table, scenario definitions, standards register

---

### Step 2: Compile Inputs and Assumptions
1. Compile vessel data (displacement, dimensions, source)
2. Determine approach velocities with justification (from ER, site conditions, standards)
3. Select berthing coefficients (Cm, Ce, Cc, Cs) from standards
4. Determine safety factor per ER/standards
5. Document all assumptions in assumptions register

**Outputs:** Vessel data table, velocity selection table, coefficient table, assumptions register

---

### Step 3: Execute Calculations
1. Calculate berthing energy for each design case using kinetic energy formula
2. Apply safety factor
3. Identify governing case (maximum factored energy)
4. Document calculation limitations

**Outputs:** Calculation sheets, governing case statement

---

### Step 4: Prepare Report
1. Draft executive summary with governing results
2. Compile design basis chapter
3. Include calculation appendix
4. Include assumptions register appendix
5. Include input register appendix

**Outputs:** Draft report with all required sections

---

### Step 5: QA/QC Review
1. Submit for independent check
2. Address review comments
3. Obtain review sign-off

**Outputs:** Review record, comment disposition log, updated report

---

### Step 6: Finalize and Issue
1. Finalize per document control procedures
2. Issue under controlled transmittal
3. Update `_STATUS.md` to ISSUED
4. Archive records

**Outputs:** Final report, transmittal, updated status

---

## Requirement Coverage Matrix

| Req ID | Step(s) | Evidence |
|---|---|---|
| R-001 | 3, 4 | Complete report with all sections |
| R-002 | 1, 2 | Vessel/scenario documentation |
| R-003 | 1, 2, 3 | Methodology and calculations |
| R-004 | 1 | ER clause mapping |
| R-005 | 2, 4 | Input/assumptions registers |
| R-006 | 5, 6 | QA/QC and control records |

---

## Verification Checkpoints

| Checkpoint | Verification | Hold Point |
|---|---|---|
| After Step 1 | Design basis complete, ER-consistent | No |
| After Step 3 | Calculations checked, governing case identified | No |
| After Step 5 | QA review complete, comments closed | **Yes** |
| After Step 6 | Controlled issue complete | No |

---

## Sources

- Decomposition line 286
- ER Vol 2 Parts 1-2 *(TBD)*
- `Specification.md` R-001 through R-006
