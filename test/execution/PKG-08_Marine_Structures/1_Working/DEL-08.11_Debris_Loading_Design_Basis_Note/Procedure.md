# Procedure: DEL-08.11 Debris Loading Design Basis Note

## Purpose

Define repeatable workflow for producing **Debris Loading Design Basis Note** for design verification and approvals.

**Deliverable intent:** Provides project management/control documentation for debris loading design basis note required by the ERs. *(Source: Decomposition line 291)*

---

## Prerequisites

**Dependency mode:** NOT_TRACKED

**Required Inputs (TBD):**

| Input | Source | Status |
|---|---|---|
| Current velocity | DEL-08.10 | **TBD** |
| Structure layout | DEL-08.01 | **TBD** |
| ER debris requirements | ER | **TBD** |
| Load case conventions | Project basis | **TBD** |

---

## Procedure Steps

### Step 1: Establish Requirements
1. Extract ER clauses for debris loading
2. Identify applicable standards
3. Confirm project load case conventions
4. Identify structures requiring debris design

**Outputs:** ER register, standards register, conventions, structure list

---

### Step 2: Characterize Debris
1. Identify debris types for site (logs, trees, etc.)
2. Determine design debris mass from ER/standards
3. Determine design debris dimensions
4. Determine impact velocity from DEL-08.10 current
5. Determine impact duration from standards/judgment
6. Define impact height range

**Outputs:** Debris type list, mass/dimensions, velocity/duration, height range

---

### Step 3: Define Load Cases
1. Define normal debris impact case
2. Define extreme debris impact case
3. Define debris accumulation case (if applicable)
4. Define concurrent conditions for each
5. Assign load case designations

**Outputs:** Load case definitions, load case table

---

### Step 4: Document Applicability
1. Define applicable structures (piles, trestle, etc.)
2. Define exposure zones on each structure
3. Document exclusions with rationale

**Outputs:** Structure list, exposure zones, exclusions

---

### Step 5: Prepare Document
1. Draft introduction and design basis
2. Compile debris characterization section
3. Compile load cases section with summary table
4. Compile applicability section
5. List assumptions with rationale

**Outputs:** Draft document

---

### Step 6: QA/QC Review
1. Submit for independent check
2. Address comments
3. Obtain sign-off

**Outputs:** Review record, updated document

---

### Step 7: Issue and Control
1. Finalize per document control
2. Issue with transmittal
3. Update `_STATUS.md`
4. Archive

**Outputs:** Final document, transmittal

---

## Requirement Coverage Matrix

| Req ID | Step(s) | Evidence |
|---|---|---|
| R-001 | 5 | Design basis and assumptions |
| R-002 | 2, 5 | Debris characterization |
| R-003 | 3, 5 | Load cases defined |
| R-004 | 4, 5 | Applicability documented |
| R-005 | 1 | ER compliance |
| R-006 | 6, 7 | QA/QC and control |

---

## Verification Checkpoints

| Checkpoint | Hold Point |
|---|---|
| After Step 2: Debris parameters complete | No |
| After Step 3: Load cases complete | No |
| After Step 5: Document complete | No |
| After Step 6: QA review complete | **Yes** |
| After Step 7: Controlled issue | No |

---

## Sources

- Decomposition line 291
- `Specification.md` R-001 through R-006
